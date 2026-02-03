import pandas as pd
import os
from .models import Faculty, FacultyAllocation, FacultyRotationState, FacultyAlternationRequest
from apps.exams.models import Student, Dataset
from django.db import transaction
from django.utils import timezone
from apps.exams.utils import normalize_department_name


FACULTY_DATASET_PATH = r"D:\AFS\FACULTY_DATASET(MODIFIED).xlsx"

def normalize_designation(designation):
    """
    Normalizes faculty designation to a canonical format.
    Handles extra spaces, dots, and common typos.
    Canonical Output: ASST.PROF, ASSO.PROF, PROFESSOR.
    """
    if not designation:
        return ""
    
    # 1. Basic cleaning: lowercase, strip, and remove all interior spaces
    raw = str(designation).strip().lower()
    # Remove all spaces and dots for comparison
    clean = raw.replace(' ', '').replace('.', '')
    
    # 2. Map cleaned versions to canonical forms
    if any(x in clean for x in ['assistant', 'asst', 'ast', 'rpof']): # 'rpof' handles 'asst.rpof'
        return "ASST.PROF"
    
    if any(x in clean for x in ['associate', 'asso', 'aso']):
        return "ASSO.PROF"
    
    if 'professor' in clean or 'prof' in clean:
        # Check this after assistant/associate to avoid false positives
        return "PROFESSOR"
    
    # 3. Final fallback: If it's already a known short form (no dots/spaces)
    if clean.upper() in ["ASSTPROF", "ASSOPROF", "PROFESSOR"]:
        if clean.upper() == "ASSTPROF": return "ASST.PROF"
        if clean.upper() == "ASSOPROF": return "ASSO.PROF"
        return "PROFESSOR"

    raise ValueError(f"Invalid designation: {designation}")

def get_faculty_sheet_data(department):
    """
    Reads faculty data from the Excel sheet corresponding to the department.
    """
    if not os.path.exists(FACULTY_DATASET_PATH):
        raise FileNotFoundError(f"Faculty dataset not found at {FACULTY_DATASET_PATH}")
    
    # Map canonical department name to sheet name if they differ
    sheet_name_map = {
        'AI&ML': 'AIML',
        'AI&DS': 'AIDS',
        'ARTIFICIAL INTELLIGENCE & DATA SCIENCE': 'AIDS',
        'ARTIFICIAL INTELLIGENCE AND DATA SCIENCE': 'AIDS',
        'CSE': 'CSE',
        'COMPUTER SCIENCE AND ENGINEERING': 'CSE',
        'ECE': 'ECE',
        'ELECTRONICS AND COMMUNICATION ENGINEERING': 'ECE',
        'ELECTRONICS AND COMMUNICATION ENG': 'ECE',
        'MECH': 'MECH',
        'MECHANICAL ENGINEERING': 'MECH',
        'CYS': 'CYS',
        'CSBS': 'CSBS',
        'MBA': 'MBA',
        'MASTER OF BUSINESS ADMINISTRATION': 'MBA',
        'IT': 'IT',
        'S&H': 'S&H',
        'SCIENCE & HUMANITIES': 'S&H',
        'SCIENCE & HUMANITIES (PHYSICS)': 'S&H',
        'SCIENCE & HUMANITIES (CHEMISTRY)': 'S&H',
        'SCIENCE & HUMANITIES (MATHS)': 'S&H',
        'SCIENCE & HUMANITIES (ENGLISH)': 'S&H',
        'BE CSE CYS': 'CYS', # Handle specific variant
        'B.TECH IT': 'IT',
        'INFORMATION TECHNOLOGY': 'IT',
    }
    
    # Try the canonical name first, then the mapped name
    try:
        xl = pd.ExcelFile(FACULTY_DATASET_PATH)
        # Normalize input department for lookup
        dept_key = str(department).strip().upper()
        sheet_name = sheet_name_map.get(dept_key, department)
        
        if sheet_name not in xl.sheet_names:
            # Robust fallback: check if any Excel sheet name is contained within the department string
            # OR if the department string contains any Excel sheet name
            # e.g., "BE CSE CyS" contains "CYS"
            clean_dept = dept_key.replace(' ', '').replace('&', '')
            for s in xl.sheet_names:
                clean_s = s.upper().replace(' ', '').replace('&', '')
                if clean_s in clean_dept or clean_dept in clean_s:
                    sheet_name = s
                    break
            
            if sheet_name not in xl.sheet_names:
                # Fallback for IT if it's not present
                if department == 'IT' and 'IT' not in xl.sheet_names:
                     potential = [s for s in xl.sheet_names if 'IT' in s]
                     if potential:
                         sheet_name = potential[0]
                
                if sheet_name not in xl.sheet_names:
                    raise ValueError(f"Sheet for department '{department}' not found in Excel. Available: {', '.join(xl.sheet_names)}")
        
        df = pd.read_excel(FACULTY_DATASET_PATH, sheet_name=sheet_name)
        
        # Standardize columns
        df.columns = df.columns.astype(str).str.upper().str.strip()
        
        # Expected: ['S.NO', 'EMP CODE', 'NAME', 'GENDER', 'DEPT', 'DESIGNATION', 'DOJ', 'MOBILE NUMBER', 'KITE MAIL ID']
        mapping = {
            'EMP CODE': 'register_no',
            'NAME': 'name',
            'DEPT': 'department',
            'DESIGNATION': 'designation'
        }
        
        # Check if required columns exist
        missing = [col for col in mapping.keys() if col not in df.columns]
        if missing:
             # Try fuzzy match if exact match fails
             for col in df.columns:
                 if ('EMP' in col or 'CODE' in col) and 'register_no' not in df.columns:
                     mapping[col] = 'register_no'
                 if 'NAME' in col and 'name' not in df.columns:
                     mapping[col] = 'name'
                 if 'DEPT' in col and 'department' not in df.columns:
                     mapping[col] = 'department'
                 if 'DESIGNATION' in col and 'designation' not in df.columns:
                     mapping[col] = 'designation'
        
        df = df.rename(columns=mapping)
        return df[['register_no', 'name', 'department', 'designation']]
    except Exception as e:
        raise ValueError(f"Error reading faculty data for {department}: {str(e)}")

@transaction.atomic
def run_faculty_allocation(dept_counts, date, session, designation):
    """
    Main allocation algorithm.
    dept_counts: dict { department_name: count }
    date: Date object
    session: string ('FN' or 'AN')
    session: string ('FN' or 'AN')
    designation: string ('Associate Professor', 'Assistant Professor')
    """
    from .models import FacultyAllocationStatus
    
    # Defensive validation for restricted designations
    allowed_designations = ['ASST.PROF', 'ASSO.PROF', 'PROFESSOR']
    normalized_requested = normalize_designation(designation)
    if normalized_requested not in allowed_designations:
        raise ValueError(f"Selection of '{designation}' is not allowed. Please select Professor, Associate or Assistant Professor.")

    # 0. Check if already confirmed
    status_obj, _ = FacultyAllocationStatus.objects.get_or_create(exam_date=date, session=session)
    if status_obj.is_confirmed:
        raise ValueError(f"Allocation for {date} ({session}) is already locked/confirmed.")

    # 1. Clear existing unconfirmed allocations for this date and session
    FacultyAllocation.objects.filter(exam_date=date, session=session, is_confirmed=False).delete()

    # 2. Get target dataset (Latest uploaded, even if not active)
    active_dataset = Dataset.objects.filter(is_active=True).first()
    if not active_dataset:
        active_dataset = Dataset.objects.order_by('-uploaded_at').first()
        
    if not active_dataset:
        raise ValueError("No seating plan dataset found. Please upload one first.")
        
    unique_halls = Student.objects.filter(dataset=active_dataset, exam_date=date, session=session)\
        .values_list('hall_no', flat=True).distinct().order_by('hall_no')
    
    unique_halls_list = list(unique_halls)
    total_halls = len(unique_halls_list)
    
    # 3. Validation: sum(counts) == number_of_unique_halls
    requested_total = sum(dept_counts.values())
    if total_halls == 0:
        # Get available dates to show user
        available_dates = Student.objects.filter(dataset=active_dataset)\
            .values('exam_date', 'session').distinct().order_by('exam_date', 'session')
        
        if available_dates.exists():
            dates_str = ', '.join([f"{d['exam_date']} ({d['session']})" for d in available_dates[:5]])
            raise ValueError(f"No exam halls found for {date} ({session}). Available dates in dataset: {dates_str}")
        else:
            raise ValueError(f"No exam halls found for {date} ({session}). The active dataset appears to be empty.")
    
    if requested_total != total_halls:
        raise ValueError(f"Validation failed: Sum of faculty counts ({requested_total}) must equal number of halls ({total_halls}).")

    # 4. Extract faculties based on rotation (Preview mode - don't update state)
    selected_faculties = []
    
    for dept_name in sorted(dept_counts.keys()):
        if dept_name.upper().strip() == 'IT':
            continue
            
        count = dept_counts[dept_name]
        if count <= 0:
            continue
            
        df = get_faculty_sheet_data(dept_name)
        
        # Filter by designation using normalization
        normalized_requested = normalize_designation(designation)
        df['normalized_designation'] = df['designation'].apply(normalize_designation)
        df = df[df['normalized_designation'] == normalized_requested]
        total_rows = len(df)
        
        if total_rows == 0:
            raise ValueError(f"Dept {dept_name} has 0 {designation}s (Normalized: {normalized_requested}). Please check the dataset.")

        if total_rows < count:
            raise ValueError(f"Dept {dept_name} has only {total_rows} {designation}s, but {count} requested.")
            
        # Get rotation state (Normalized designation used for state tracking)
        state, created = FacultyRotationState.objects.get_or_create(
            department=dept_name, 
            designation=normalized_requested
        )
        
        # Pointer logic (Bottom-up selection):
        # We start from the bottom if last_row_index is -1, 
        # picking 'count' rows sequentially upwards.
        if state.last_row_index == -1 or state.last_row_index >= total_rows:
            # If never allocated OR index is now invalid due to dataset change, 
            # start from the bottom-most possible subset
            start_index = (total_rows - count) % total_rows
        else:
            # If previous allocation exists, start from the next one upwards
            start_index = (state.last_row_index + 1) % total_rows
            
        indices = []
        for i in range(count):
            indices.append((start_index + i) % total_rows)
            
        dept_faculties_df = df.iloc[indices]
        
        for _, row in dept_faculties_df.iterrows():
            reg_no = str(row['register_no']).strip().upper()
            faculty, _ = Faculty.objects.get_or_create(
                register_no=reg_no,
                defaults={
                    'name': str(row['name']),
                    'department': str(row['department']),
                }
            )
            if _:
                faculty.set_password('Kite@123')
                faculty.save()
            selected_faculties.append(faculty)

    # 5. Mapping: Assign one faculty per hall (Unconfirmed)
    allocations = []
    for i, hall_no in enumerate(unique_halls_list):
        faculty = selected_faculties[i]
        student_info = Student.objects.filter(dataset=active_dataset, exam_date=date, session=session, hall_no=hall_no).first()
        
        allocations.append(FacultyAllocation(
            faculty=faculty,
            hall_no=hall_no,
            course_code=student_info.course_code if student_info else "N/A",
            course_title=student_info.course_title if student_info else "N/A",
            exam_date=date,
            session=session,
            is_confirmed=False # Mark as preview
        ))
        
    FacultyAllocation.objects.bulk_create(allocations)
    return FacultyAllocation.objects.filter(exam_date=date, session=session)


@transaction.atomic
def confirm_faculty_allocation(date, session):
    """
    Finalize allocation logic: updates rotation state and locks the session.
    """
    from .models import FacultyAllocationStatus
    
    status_obj, _ = FacultyAllocationStatus.objects.get_or_create(exam_date=date, session=session)
    if status_obj.is_confirmed:
        raise ValueError("Allocation already confirmed.")
        
    allocations = FacultyAllocation.objects.filter(exam_date=date, session=session, is_confirmed=False)
    if not allocations.exists():
        raise ValueError("No preview allocations found to confirm.")
        
    # Group by dept and designation to update rotation pointers
    # Note: We need to know what designation was used. 
    # For now, we assume all in one batch have the same designation or we look it up.
    
    # Update rotation state
    for alloc in allocations:
        # We need the index in the Excel sheet. 
        # This is a bit redundant but ensures fair rotation.
        dept = alloc.faculty.department
        # Get designation from Excel (safest way to ensure match)
        df = get_faculty_sheet_data(dept)
        # Find the designation for this faculty
        faculty_row = df[df['register_no'].astype(str).str.strip().str.upper() == alloc.faculty.register_no.strip().upper()]
        if faculty_row.empty:
            continue
        designation = faculty_row.iloc[0]['designation']
        
        # Filter df to relevant designation the same way allocation does
        normalized_fac_designation = normalize_designation(faculty_row.iloc[0]['designation'])
        df['normalized_designation'] = df['designation'].apply(normalize_designation)
        designation_df = df[df['normalized_designation'] == normalized_fac_designation].reset_index(drop=True)
        
        # Find new index
        new_row_idx_search = designation_df[designation_df['register_no'].astype(str).str.strip().str.upper() == alloc.faculty.register_no.strip().upper()]
        if not new_row_idx_search.empty:
            new_idx = new_row_idx_search.index[0]
            state, _ = FacultyRotationState.objects.get_or_create(
                department=dept, 
                designation=normalized_fac_designation
            )
            # We want to set the pointer to the last index touched
            state.last_row_index = new_idx
            state.save()

    # Mark all as confirmed
    allocations.update(is_confirmed=True)
    status_obj.is_confirmed = True
    status_obj.save()
    
    return True


@transaction.atomic
def replace_faculty(allocation_id, reason, update_rotation=False):
    """
    Emergency replacement logic.
    Identifies the next available faculty in the same department and reassigns the hall.
    If update_rotation is True, the FacultyRotationState pointer is advanced to the new faculty.
    """
    allocation = FacultyAllocation.objects.select_for_update().get(id=allocation_id)
    if allocation.is_replaced:
        raise ValueError("This duty has already been replaced.")
    
    dept_name = allocation.faculty.department
    original_reg_no = allocation.faculty.register_no.strip().upper()
    
    df = get_faculty_sheet_data(dept_name)
    # Get the designation of the faculty being replaced
    faculty_row = df[df['register_no'].astype(str).str.strip().str.upper() == original_reg_no]
    if faculty_row.empty:
        raise ValueError(f"Original faculty {original_reg_no} not found in department {dept_name} data.")
    raw_designation = faculty_row.iloc[0]['designation']
    normalized_designation = normalize_designation(raw_designation)
    
    # Filter df by the same normalized designation
    df['normalized_designation'] = df['designation'].apply(normalize_designation)
    designation_df = df[df['normalized_designation'] == normalized_designation].reset_index(drop=True)
    total_designation_rows = len(designation_df)
    
    if total_designation_rows <= 1:
        raise ValueError(f"No other {normalized_designation}s found in {dept_name} for replacement.")
    
    state, _ = FacultyRotationState.objects.get_or_create(
        department=dept_name, 
        designation=normalized_designation
    )
    
    # Safety check for index
    current_idx = state.last_row_index
    if current_idx == -1 or current_idx >= total_designation_rows:
        current_idx = 0
    
    found_replacement = None
    
    # Search for first faculty from current pointer onwards who is available
    for i in range(1, total_designation_rows): 
        idx = (current_idx + i) % total_designation_rows
        row = designation_df.iloc[idx]
        reg_no = str(row['register_no']).strip().upper()
        
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
            
            # Mark original as replaced
            allocation.is_replaced = True
            allocation.reason_for_unavailability = reason
            allocation.replaced_by = replacement_faculty
            allocation.save()

            if update_rotation:
                state.last_row_index = idx
                state.save()
            
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


def request_alternation(faculty_reg_no, allocation_id, reason):
    """
    Submits an alternation request for a faculty member.
    """
    try:
        faculty = Faculty.objects.get(register_no=faculty_reg_no.strip().upper())
        allocation = FacultyAllocation.objects.get(id=allocation_id, faculty=faculty)
        
        # Check if already replaced or request exists
        if allocation.is_replaced:
            raise ValueError("This duty has already been reassigned.")
            
        # Check for existing pending request
        existing = FacultyAlternationRequest.objects.filter(faculty=faculty, allocation=allocation).first()
        if existing:
            if existing.status == FacultyAlternationRequest.PENDING:
                raise ValueError("You have already submitted a pending alternation request for this assignment.")
            elif existing.status == FacultyAlternationRequest.APPROVED:
                raise ValueError("This request has already been approved.")
            # If rejected, they might want to re-submit with a better reason? 
            # For now, let's allow unique_together to handle it or block it.
            # User wants unique_together = (faculty, allocation) which I added.
            # So they can't re-submit if a record exists.
            raise ValueError(f"An alternation request already exists for this assignment (Status: {existing.status}).")
            
        request_obj = FacultyAlternationRequest.objects.create(
            faculty=faculty,
            allocation=allocation,
            reason=reason
        )
             
        return request_obj
    except Faculty.DoesNotExist:
        raise ValueError("Faculty not found.")
    except FacultyAllocation.DoesNotExist:
        raise ValueError("Allocation not found or does not belong to you.")


@transaction.atomic
def reject_alternation(request_id, admin_user):
    """
    Rejects an alternation request.
    """
    request_obj = FacultyAlternationRequest.objects.select_for_update().get(id=request_id)
    if request_obj.status != FacultyAlternationRequest.PENDING:
        raise ValueError(f"Request is already {request_obj.status}.")
        
    request_obj.status = FacultyAlternationRequest.REJECTED
    request_obj.approved_by = admin_user
    request_obj.save()
    return request_obj


@transaction.atomic
def approve_alternation(request_id, admin_user):
    """
    Approves an alternation request and performs the replacement.
    """
    request_obj = FacultyAlternationRequest.objects.select_for_update().get(id=request_id)
    if request_obj.status != FacultyAlternationRequest.PENDING:
        raise ValueError(f"Request is already {request_obj.status}.")
        
    allocation = request_obj.allocation
    
    # Perform replacement using existing deterministic logic
    # We update the rotation pointer here as requested by user
    new_allocation = replace_faculty(allocation.id, request_obj.reason, update_rotation=True)
    
    # Update request status
    request_obj.status = FacultyAlternationRequest.APPROVED
    request_obj.approved_by = admin_user
    request_obj.approved_at = timezone.now()
    request_obj.save()
    
    return new_allocation
