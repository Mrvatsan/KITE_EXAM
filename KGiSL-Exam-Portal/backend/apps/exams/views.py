from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Dataset, Student
from .utils import clean_and_parse_excel
from django.utils import timezone
import pandas as pd

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'student') # 'student' or 'admin'

        if role == 'admin':
            user = authenticate(username=username, password=password)
            if user and user.is_superuser:
                return Response({'token': 'admin-dummy-token', 'role': 'admin', 'username': user.username}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid Admin Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        else: # Student Login
            # Check active dataset first
            active_dataset = Dataset.objects.filter(is_active=True).first()
            if not active_dataset:
                return Response({'error': 'No active exam info found. Pending for admin access.'}, status=status.HTTP_403_FORBIDDEN)
            
            try:
                # Filter by active dataset and credentials
                student = Student.objects.get(register_no=username, password=password, dataset=active_dataset)
                
                # Clean hall and seat numbers (remove decimal points from Excel numeric values)
                hall_no = str(student.hall_no).strip()
                seat_no = str(student.seat_no).strip()
                
                # Convert decimal values to integers (e.g., "201.0" -> "201")
                try:
                    if '.' in hall_no:
                        hall_no = str(int(float(hall_no)))
                except (ValueError, TypeError):
                    pass  # Keep original if conversion fails
                
                try:
                    if '.' in seat_no:
                        seat_no = str(int(float(seat_no)))
                except (ValueError, TypeError):
                    pass  # Keep original if conversion fails
                
                # Format exam date properly (from database DateField)
                exam_date_str = student.exam_date.strftime('%Y-%m-%d') if student.exam_date else None
                
                return Response({
                    'role': 'student',
                    'name': student.name,
                    'register_no': student.register_no,
                    'course_code': student.course_code,
                    'course_title': student.course_title,
                    'exam_date': exam_date_str,  # Properly formatted from database
                    'session': student.session,
                    'hall_no': hall_no,  # Cleaned (no decimals)
                    'seat_no': seat_no   # Cleaned (no decimals)
                }, status=status.HTTP_200_OK)
            except Student.DoesNotExist:
                return Response({'error': 'Invalid Credentials or Student not found in active list'}, status=status.HTTP_401_UNAUTHORIZED)


class DatasetUploadView(APIView):
    def post(self, request):
        # Only allow simpler validation for now (assume admin checks handled via token or session, but for quick prototype we skip strict auth check here or add simple one if needed)
        # For full security we'd check headers.
        
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = clean_and_parse_excel(file)
            
            # Create Dataset
            dataset = Dataset.objects.create(file=file, is_active=False)
            
            # Create Students
            students_to_create = []
            for _, row in df.iterrows():
                # Format Date if needed
                e_date = row.get('exam_date')
                parsed_date = None
                
                # Try to parse the exam_date
                if pd.notna(e_date):
                    try:
                        # Handle string dates in YYYY-MM-DD format
                        if isinstance(e_date, str):
                            from datetime import datetime
                            parsed_date = datetime.strptime(e_date.strip(), '%Y-%m-%d').date()
                        # Handle datetime objects
                        elif hasattr(e_date, 'date'):
                            parsed_date = e_date.date()
                        # Handle pandas Timestamp
                        elif pd.api.types.is_datetime64_any_dtype(type(e_date)):
                            parsed_date = pd.to_datetime(e_date).date()
                        # Handle Excel serial numbers
                        elif isinstance(e_date, (int, float)) and e_date > 0:
                            from datetime import datetime, timedelta
                            excel_epoch = datetime(1899, 12, 30)
                            parsed_date = (excel_epoch + timedelta(days=float(e_date))).date()
                        else:
                            # Last resort: try pandas
                            parsed_date = pd.to_datetime(e_date, errors='coerce').date()
                    except Exception as parse_error:
                        print(f"DEBUG: Date parsing error for value '{e_date}' (type: {type(e_date)}): {parse_error}")
                        parsed_date = None
                
                # Clean hall and seat numbers (remove .0 from Excel decimal numbers)
                hall_no = str(row.get('hall_no', '')).strip()
                seat_no = str(row.get('seat_no', '')).strip()
                
                try:
                    if '.' in hall_no:
                        hall_no = str(int(float(hall_no)))
                except:
                    pass
                try:
                    if '.' in seat_no:
                        seat_no = str(int(float(seat_no)))
                except:
                    pass

                students_to_create.append(Student(
                    dataset=dataset,
                    register_no=str(row.get('register_no', '')),
                    name=str(row.get('name', '')),
                    course_code=str(row.get('course_code', '')),
                    course_title=str(row.get('course_title', '')),
                    exam_date=parsed_date, 
                    session=str(row.get('session', '')),
                    hall_no=hall_no,
                    seat_no=seat_no
                ))
            
            Student.objects.bulk_create(students_to_create)
            
            return Response({'message': 'Dataset uploaded successfully', 'students_count': len(students_to_create), 'dataset_id': dataset.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DatasetListView(APIView):
    def get(self, request):
        datasets = Dataset.objects.all().order_by('-uploaded_at')
        data = []
        for d in datasets:
            data.append({
                'id': d.id,
                'uploaded_at': d.uploaded_at,
                'is_active': d.is_active,
                'student_count': d.students.count()
            })
        return Response(data)

class ToggleDatasetView(APIView):
    def post(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
            # Deactivate all others if activating this one
            if not dataset.is_active:
                Dataset.objects.update(is_active=False)
                dataset.is_active = True
            else:
                dataset.is_active = False # Toggle off
            dataset.save()
            return Response({'message': f"Dataset {'activated' if dataset.is_active else 'deactivated'}", 'is_active': dataset.is_active})
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

class DeleteStudentsView(APIView):
    def delete(self, request):
        Dataset.objects.all().delete() # Cascades to students
        return Response({'message': 'All data cleared'})


# ============ HALL TICKET VIEWS ============

class HallTicketView(APIView):
    """
    Student endpoint to retrieve hall ticket data.
    Automatically determines department from register number.
    Auto-loads hall ticket data from pre-existing Excel file if database is empty.
    Returns all semesters' exam data for the student's department.
    """
    def get(self, request):
        from .models import HallTicketExam, Student
        from .utils import get_department_from_register_no, parse_hall_ticket_excel
        import os
        
        # Auto-load Excel data if database is empty
        if not HallTicketExam.objects.exists():
            try:
                # Path to the pre-existing hall ticket Excel file
                # views.py is in apps/exams/, so we need to go up 3 levels to reach backend root
                # os.path.dirname(os.path.dirname(os.path.dirname(__file__))) -> backend root
                backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                excel_path = os.path.join(backend_dir, 'HALL_TICKET.xlsx')
                
                print(f"Looking for Hall Ticket file at: {excel_path}")
                
                if os.path.exists(excel_path):
                    with open(excel_path, 'rb') as excel_file:
                        records = parse_hall_ticket_excel(excel_file)
                        if records:
                            exam_objects = [HallTicketExam(**record) for record in records]
                            HallTicketExam.objects.bulk_create(exam_objects)
                            print(f"Auto-loaded {len(records)} hall ticket records from Excel file")
            except Exception as e:
                print(f"Error auto-loading hall ticket data: {str(e)}")
        
        # Get register number from query params
        register_no = request.GET.get('register_no')
        
        if not register_no:
            return Response({'error': 'Register number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Identify department from register number
        department = get_department_from_register_no(register_no)
        
        if not department:
            return Response({'error': 'Invalid register number format or unknown department'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get student details from active dataset
        try:
            active_dataset = Dataset.objects.filter(is_active=True).first()
            if not active_dataset:
                return Response({'error': 'No active dataset found'}, status=status.HTTP_403_FORBIDDEN)
            
            student = Student.objects.get(register_no=register_no, dataset=active_dataset)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found in active dataset'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get all exam data for this department, grouped by semester
        exams = HallTicketExam.objects.filter(department=department).order_by('semester', 'exam_date', 'session')
        
        if not exams.exists():
            return Response({'error': f'No hall ticket data found for department {department}'}, status=status.HTTP_404_NOT_FOUND)
        
        # Group exams by semester
        semesters_data = {}
        for exam in exams:
            sem = exam.semester
            if sem not in semesters_data:
                semesters_data[sem] = []
            
            semesters_data[sem].append({
                'course_code': exam.course_code,
                'course_title': exam.course_title,
                'exam_date': exam.exam_date.strftime('%d-%m-%Y'),
                'session': exam.session
            })
        
        # Return student info and exam data
        return Response({
            'student': {
                'name': student.name,
                'register_no': student.register_no,
                'department': department
            },
            'semesters': semesters_data
        }, status=status.HTTP_200_OK)


class AvailableExamDatesView(APIView):
    """
    Returns all available exam dates and sessions from the active dataset.
    Useful for faculty allocation to know which dates can be allocated.
    """
    def get(self, request):
        active_dataset = Dataset.objects.filter(is_active=True).first()
        
        if not active_dataset:
            return Response({
                'available_dates': [],
                'message': 'No active dataset found'
            }, status=status.HTTP_200_OK)
        
        # Get all unique date-session combinations
        dates_sessions = Student.objects.filter(dataset=active_dataset)\
            .values('exam_date', 'session').distinct().order_by('exam_date', 'session')
        
        available_dates = []
        for ds in dates_sessions:
            hall_count = Student.objects.filter(
                dataset=active_dataset,
                exam_date=ds['exam_date'],
                session=ds['session']
            ).values('hall_no').distinct().count()
            
            available_dates.append({
                'date': ds['exam_date'].strftime('%Y-%m-%d'),
                'session': ds['session'],
                'halls': hall_count
            })
        
        return Response({
            'available_dates': available_dates,
            'total_count': len(available_dates)
        }, status=status.HTTP_200_OK)
