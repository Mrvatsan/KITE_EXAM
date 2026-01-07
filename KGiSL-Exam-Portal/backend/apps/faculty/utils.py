import pandas as pd
import os
from .models import Faculty, FacultyAllocation, FacultyRotationState
from apps.exams.models import Student, Dataset
from django.db import transaction
from django.utils import timezone
from apps.exams.utils import normalize_department_name


FACULTY_DATASET_PATH = r"D:\AFS\FACULTY_DATASET (3).xlsx"

def get_faculty_sheet_data(department):
    """
    Reads faculty data from the Excel sheet corresponding to the department.
    """
    if not os.path.exists(FACULTY_DATASET_PATH):
        raise FileNotFoundError(f"Faculty dataset not found at {FACULTY_DATASET_PATH}")
    
    # Map canonical department name to sheet name if they differ
    # Based on inspection: ['AIML', 'CYS', 'AIDS', 'CSE', 'MECH', 'ECE', 'CSBS', 'MBA', 'S&H']
    sheet_name_map = {
        'AI&ML': 'AIML',
        'AI&DS': 'AIDS',
        'CSE': 'CSE',
        'ECE': 'ECE',
        'MECH': 'MECH',
        'CYS': 'CYS',
        'CSBS': 'CSBS',
        'IT': 'IT', # IT was missing in my inspection but usually present
    }
    
    # Try the canonical name first, then the mapped name
    try:
        xl = pd.ExcelFile(FACULTY_DATASET_PATH)
        sheet_name = sheet_name_map.get(department, department)
        
        if sheet_name not in xl.sheet_names:
            # Fallback for IT if it's not present (sometimes it's under CSE or separate)
            if department == 'IT' and 'IT' not in xl.sheet_names:
                 # Check if there's any sheet that looks like IT
                 potential = [s for s in xl.sheet_names if 'IT' in s]
                 if potential:
                     sheet_name = potential[0]
            
            if sheet_name not in xl.sheet_names:
                raise ValueError(f"Sheet for department '{department}' not found in Excel.")
        
        df = pd.read_excel(FACULTY_DATASET_PATH, sheet_name=sheet_name)
        
        # Standardize columns
        df.columns = df.columns.astype(str).str.upper().str.strip()
        
        # Expected: ['S.NO', 'EMP CODE', 'NAME', 'GENDER', 'DEPT', 'DESIGNATION', 'DOJ', 'MOBILE NUMBER', 'KITE MAIL ID']
        mapping = {
            'EMP CODE': 'register_no',
            'NAME': 'name',
            'DEPT': 'department'
        }
        
        # Check if required columns exist
        missing = [col for col in mapping.keys() if col not in df.columns]
        if missing:
             # Try fuzzy match if exact match fails
             for col in df.columns:
                 if 'EMP' in col or 'CODE' in col and 'register_no' not in df.columns:
                     mapping[col] = 'register_no'
                 if 'NAME' in col and 'name' not in df.columns:
                     mapping[col] = 'name'
                 if 'DEPT' in col and 'department' not in df.columns:
                     mapping[col] = 'department'
        
        df = df.rename(columns=mapping)
        return df[['register_no', 'name', 'department']]
    except Exception as e:
        raise ValueError(f"Error reading faculty data for {department}: {str(e)}")

@transaction.atomic
def run_faculty_allocation(dept_counts, date, session):
    """
    Main allocation algorithm.
    dept_counts: dict { department_name: count }
    date: Date object
    session: string ('FN' or 'AN')
    """
    # 1. Clear existing allocations for this date and session to handle re-uploads/re-allocation
    # This ensures that if a new dataset is uploaded or counts are updated, the faculty see fresh data.
    FacultyAllocation.objects.filter(exam_date=date, session=session).delete()

    # 2. Get unique halls from active dataset
    active_dataset = Dataset.objects.filter(is_active=True).first()
    if not active_dataset:
        raise ValueError("No active student dataset found.")
        
    unique_halls = Student.objects.filter(dataset=active_dataset, exam_date=date, session=session)\
        .values_list('hall_no', flat=True).distinct().order_by('hall_no')
    
    unique_halls_list = list(unique_halls)
    total_halls = len(unique_halls_list)
    
    # 3. Validation: sum(counts) == number_of_unique_halls
    requested_total = sum(dept_counts.values())
    if requested_total != total_halls:
        raise ValueError(f"Validation failed: Sum of faculty counts ({requested_total}) must equal number of halls ({total_halls}).")

    # 4. Extract faculties based on rotation
    selected_faculties = []
    
    # Sort departments to ensure deterministic behavior
    for dept_name in sorted(dept_counts.keys()):
        # Issue 2: Forcefully exclude IT Department from allocation algorithm
        if dept_name.upper().strip() == 'IT':
            continue
            
        count = dept_counts[dept_name]
        if count <= 0:
            continue
            
        df = get_faculty_sheet_data(dept_name)
        total_rows = len(df)
        
        if total_rows < count:
            raise ValueError(f"Department {dept_name} has only {total_rows} faculty members, but {count} were requested.")
            
        # Get rotation state
        state, created = FacultyRotationState.objects.get_or_create(department=dept_name)
        
        # Pointer logic:
        # If first time (last_row_index == -1), start such that we pick the last 'count' rows
        # "Allocation starts from the last faculty row... If admin selects N faculty -> last N are chosen."
        if state.last_row_index == -1:
            start_index = (total_rows - count) % total_rows
        else:
            start_index = (state.last_row_index + 1) % total_rows
            
        indices = []
        for i in range(count):
            indices.append((start_index + i) % total_rows)
            
        dept_faculties_df = df.iloc[indices]
        
        for _, row in dept_faculties_df.iterrows():
            # Issue 3: Normalize register_no (Uppercase, Trim)
            reg_no = str(row['register_no']).strip().upper()
            
            # Create or get Faculty record
            faculty, _ = Faculty.objects.get_or_create(
                register_no=reg_no,
                defaults={
                    'name': str(row['name']),
                    'department': str(row['department']),
                }
            )
            # Ensure password is set if new
            if _:
                faculty.set_password('Kite@123')
                faculty.save()
                
            selected_faculties.append(faculty)
            
        # Update pointer to the last index selected
        state.last_row_index = indices[-1]
        state.save()

    # 5. Mapping: Assign one faculty per hall
    # Mapping must be deterministic: halls are sorted, faculties are collected per dept (which are also sorted)
    allocations = []
    for i, hall_no in enumerate(unique_halls_list):
        faculty = selected_faculties[i]
        
        # Get course details for this hall (Assumes one course per hall/session as per system rules)
        student_info = Student.objects.filter(dataset=active_dataset, exam_date=date, session=session, hall_no=hall_no).first()
        
        allocations.append(FacultyAllocation(
            faculty=faculty,
            hall_no=hall_no,
            course_code=student_info.course_code if student_info else "N/A",
            course_title=student_info.course_title if student_info else "N/A",
            exam_date=date,
            session=session
        ))
        
    FacultyAllocation.objects.bulk_create(allocations)
    return FacultyAllocation.objects.filter(exam_date=date, session=session)


@transaction.atomic
def replace_faculty(allocation_id, reason):
    """
    Emergency replacement logic.
    Identifies the next available faculty in the same department and reassigns the hall.
    """
    allocation = FacultyAllocation.objects.select_for_update().get(id=allocation_id)
    if allocation.is_replaced:
        raise ValueError("This duty has already been replaced.")
        
    dept_name = allocation.faculty.department
    df = get_faculty_sheet_data(dept_name)
    total_rows = len(df)
    
    state, _ = FacultyRotationState.objects.get_or_create(department=dept_name)
    
    found_replacement = None
    original_reg_no = allocation.faculty.register_no
    
    # Search for first faculty from current pointer onwards who is available
    for i in range(1, total_rows): 
        idx = (state.last_row_index + i) % total_rows
        row = df.iloc[idx]
        reg_no = str(row['register_no'])
        
        if reg_no == original_reg_no:
            continue
            
        # Check if already assigned for this session
        is_assigned = FacultyAllocation.objects.filter(
            faculty__register_no=reg_no,
            exam_date=allocation.exam_date,
            session=allocation.session
        ).exists()
        
        if not is_assigned:
            replacement_name = str(row['name'])
            replacement_faculty, _ = Faculty.objects.get_or_create(
                register_no=reg_no,
                defaults={'name': replacement_name, 'department': dept_name}
            )
            if _:
                replacement_faculty.set_password('Kite@123')
                replacement_faculty.save()
            
            # Update pointers? No, we won't move the main rotation pointer for an emergency replacement
            # to keep the regular rotation fair for the 'next day'.
            
            # Mark original as replaced
            allocation.is_replaced = True
            allocation.reason_for_unavailability = reason
            allocation.replaced_by = replacement_faculty
            allocation.save()
            
            # Create new allocation for replacement
            return FacultyAllocation.objects.create(
                faculty=replacement_faculty,
                hall_no=allocation.hall_no,
                course_code=allocation.course_code,
                course_title=allocation.course_title,
                exam_date=allocation.exam_date,
                session=allocation.session
            )
            
    raise ValueError(f"No available replacement found in department {dept_name} for this session.")
