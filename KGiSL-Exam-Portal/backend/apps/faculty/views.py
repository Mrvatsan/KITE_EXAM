from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Faculty, FacultyToken, FacultyAllocation
from django.utils import timezone


class FacultyLoginView(APIView):
    """
    Dedicated login view for Faculty members.
    Verifies credentials and returns a secure token.
    """
    def post(self, request):
        register_no = str(request.data.get('register_no', '')).strip().upper()
        password = request.data.get('password')

        if not register_no or not password:
            return Response(
                {'error': 'Register number and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            faculty = Faculty.objects.get(register_no=register_no)
            if faculty.check_password(password):
                # Create or Refresh Token
                token, created = FacultyToken.objects.get_or_create(faculty=faculty)
                
                # If token exists but is expired, regenerate it
                if not created and token.is_expired():
                    token.delete()
                    token = FacultyToken.objects.create(faculty=faculty)
                
                return Response({
                    'token': token.key,
                    'role': 'faculty',
                    'username': faculty.register_no,
                    'name': faculty.name,
                    'department': faculty.department
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Invalid Faculty Credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Faculty.DoesNotExist:
            return Response(
                {'error': 'Faculty member not found'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class FacultyLogoutView(APIView):
    """
    Dedicated logout view for Faculty members.
    Invalidates the authentication token.
    """
    def post(self, request):
        token_key = request.headers.get('Authorization')
        if token_key:
            try:
                # Assuming format "Token <key>" or just "<key>"
                key = token_key.replace('Token ', '').strip()
                token = FacultyToken.objects.get(key=key)
                token.delete()
                return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
            except FacultyToken.DoesNotExist:
                pass
        
        return Response({'message': 'Token not found or already logged out'}, status=status.HTTP_200_OK)


class FacultyProfileView(APIView):
    """
    Returns current faculty profile if authenticated.
    """
    def get(self, request):
        token_key = request.headers.get('Authorization')
        if not token_key:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            key = token_key.replace('Token ', '').strip()
            token = FacultyToken.objects.get(key=key)
            
            if token.is_expired():
                token.delete()
                return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
            
            faculty = token.faculty
            return Response({
                'name': faculty.name,
                'register_no': faculty.register_no,
                'department': faculty.department,
                'role': 'faculty'
            }, status=status.HTTP_200_OK)
            
        except FacultyToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


# ============ ADMIN FACULTY APIS ============

class AdminFacultyAllocationView(APIView):
    """
    API for admin to trigger faculty allocation.
    Input: { "dept_counts": { "CSE": 5, ... }, "date": "YYYY-MM-DD", "session": "FN" }
    """
    def post(self, request):
        dept_counts = request.data.get('dept_counts') 
        date_str = request.data.get('date')
        session = request.data.get('session')
        designation = request.data.get('designation')
        
        if not dept_counts or not date_str or not session or not designation:
            return Response(
                {'error': 'Missing required fields: dept_counts, date, session, designation'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            from .utils import run_faculty_allocation
            allocations = run_faculty_allocation(dept_counts, date_obj, session, designation)
            
            data = []
            for alloc in allocations:
                data.append({
                    'hall_no': alloc.hall_no,
                    'faculty_name': alloc.faculty.name,
                    'faculty_reg_no': alloc.faculty.register_no,
                    'department': alloc.faculty.department,
                    'course_code': alloc.course_code,
                    'course_title': alloc.course_title,
                    'is_confirmed': alloc.is_confirmed
                })
                
            return Response({
                'message': 'Preview allocation generated',
                'allocations': data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminFacultyConfirmView(APIView):
    """
    API for admin to lock/confirm faculty allocation.
    """
    def post(self, request):
        date_str = request.data.get('date')
        session = request.data.get('session')
        
        if not date_str or not session:
            return Response({'error': 'Date and session required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            from .utils import confirm_faculty_allocation
            confirm_faculty_allocation(date_obj, session)
            
            return Response({'message': 'Allocation confirmed and locked'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminFacultyResetAllocationView(APIView):
    """
    API for admin to unlock/reset faculty allocations for a specific date and session.
    """
    def post(self, request):
        date_str = request.data.get('date')
        session = request.data.get('session')
        
        if not date_str or not session:
            return Response({'error': 'Date and session required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            from .utils import reset_faculty_allocation
            count = reset_faculty_allocation(date_obj, session)
            
            return Response({
                'message': f'Allocation for {date_str} ({session}) has been reset and unlocked.',
                'deleted_count': count
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminFacultyStatusView(APIView):
    """
    API for admin to toggle faculty visibility and check status.
    """
    def get(self, request):
        date_str = request.query_params.get('date')
        session = request.query_params.get('session')
        
        if not date_str or not session:
            return Response({'error': 'Date and session required'}, status=status.HTTP_400_BAD_REQUEST)
            
        from .models import FacultyAllocationStatus
        from datetime import datetime
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        status_obj, _ = FacultyAllocationStatus.objects.get_or_create(exam_date=date_obj, session=session)
        
        return Response({
            'is_confirmed': status_obj.is_confirmed,
            'is_faculty_active': status_obj.is_faculty_active
        })

    def post(self, request):
        date_str = request.data.get('date')
        session = request.data.get('session')
        is_active = request.data.get('is_faculty_active')
        
        if not date_str or not session or is_active is None:
            return Response({'error': 'Date, session, and is_faculty_active required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            from .models import FacultyAllocationStatus
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            status_obj, _ = FacultyAllocationStatus.objects.get_or_create(exam_date=date_obj, session=session)
            status_obj.is_faculty_active = is_active
            status_obj.save()
            
            return Response({'message': f'Faculty visibility set to {is_active}'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminFacultyListView(APIView):
    """
    API for admin to view allocated faculty for a specific date and session.
    """
    def get(self, request):
        date_str = request.query_params.get('date')
        session = request.query_params.get('session')
        
        if not date_str or not session:
             return Response(
                 {'error': 'Missing date or session parameters'}, 
                 status=status.HTTP_400_BAD_REQUEST
             )
             
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            allocations = FacultyAllocation.objects.filter(
                exam_date=date_obj, 
                session=session
            ).exclude(faculty__department__iexact='IT').order_by('hall_no')
            
            data = []
            for alloc in allocations:
                data.append({
                    'id': alloc.id,
                    'hall_no': alloc.hall_no,
                    'faculty_name': alloc.faculty.name,
                    'faculty_reg_no': alloc.faculty.register_no,
                    'department': alloc.faculty.department,
                    'course_code': alloc.course_code,
                    'course_title': alloc.course_title,
                    'is_confirmed': alloc.is_confirmed,
                    'is_replaced': alloc.is_replaced,
                    'replaced_by': alloc.replaced_by.name if alloc.replaced_by else None
                })
            return Response(data)
        except Exception as e:
             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class AdminFacultyListCreateView(APIView):
    """
    API for admin to list all faculty members or create a new one.
    GET: List all faculty
    POST: Create new faculty
    """
    def get(self, request):
        faculty_list = Faculty.objects.all().order_by('department', 'name')
        data = []
        for f in faculty_list:
            data.append({
                'id': f.id,
                'name': f.name,
                'register_no': f.register_no,
                'department': f.department,
            })
        return Response(data)

    def post(self, request):
        name = request.data.get('name')
        register_no = request.data.get('register_no')
        department = request.data.get('department')
        password = request.data.get('password')

        if not all([name, register_no, department, password]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Faculty.objects.filter(register_no=register_no).exists():
            return Response({'error': 'Faculty with this Register No already exists'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            faculty = Faculty(
                name=name,
                register_no=register_no,
                department=department
            )
            faculty.set_password(password)
            faculty.save()
            
            return Response({
                'id': faculty.id,
                'name': faculty.name,
                'register_no': faculty.register_no,
                'department': faculty.department
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminFacultyDetailView(APIView):
    """
    API for admin to retrieve, update or delete a specific faculty member.
    """
    def get_object(self, pk):
        try:
            return Faculty.objects.get(pk=pk)
        except Faculty.DoesNotExist:
            return None

    def put(self, request, pk):
        faculty = self.get_object(pk)
        if not faculty:
            return Response({'error': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name')
        register_no = request.data.get('register_no')
        department = request.data.get('department')
        password = request.data.get('password') # Optional for update

        if name: faculty.name = name
        if register_no: 
            # Check if new register_no conflicts with another faculty
            if Faculty.objects.filter(register_no=register_no).exclude(pk=pk).exists():
                return Response({'error': 'Register No already exists'}, status=status.HTTP_400_BAD_REQUEST)
            faculty.register_no = register_no
        if department: faculty.department = department
        if password: faculty.set_password(password)

        faculty.save()

        return Response({
            'id': faculty.id,
            'name': faculty.name,
            'register_no': faculty.register_no,
            'department': faculty.department
        })

    def delete(self, request, pk):
        faculty = self.get_object(pk)
        if not faculty:
            return Response({'error': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)
        
        faculty.delete()
        return Response({'message': 'Faculty deleted successfully'}, status=status.HTTP_204_NO_CONTENT)






class OpenFacultyExcelView(APIView):
    """
    API that returns the Google Sheet URL.
    
    This view returns the public URL of the shared Google Sheet used for 
    Faculty Data management. The frontend uses this to open the sheet 
    in a new tab for the administrator.
    """
    def post(self, request):
        sheet_url = "https://docs.google.com/spreadsheets/d/1gRWbJIgVEuOg6nJgNIVNDmrrSwNS_-i5yfYZWw42gnE/edit?usp=sharing"
        return Response({'url': sheet_url, 'message': 'Opening Google Sheet...'}, status=status.HTTP_200_OK)


class SyncFacultyExcelView(APIView):
    """
    API to sync changes from Google Sheet (All Sheets) back to the database.
    
    Workflow:
    1. Fetches the Google Sheet as an XLSX file.
    2. Reads ALL sheets (tabs) in the workbook.
    3. Combines them into a single DataFrame.
    4. Maps 'EMP CODE' -> register_no, 'NAME' -> name, 'DEPT' -> department.
    5. Performs Upsert (Create/Update) and Delete operations.
    """
    def post(self, request):
        try:
            import pandas as pd
            import requests
            import io
            
            # Google Sheets XLSX Export URL (fetches all sheets)
            xlsx_url = "https://docs.google.com/spreadsheets/d/1gRWbJIgVEuOg6nJgNIVNDmrrSwNS_-i5yfYZWw42gnE/export?format=xlsx"
            
            print(f"Fetching data from: {xlsx_url}")
            
            response = requests.get(xlsx_url)
            response.raise_for_status()
            
            # Read all sheets
            excel_file = io.BytesIO(response.content)
            all_sheets = pd.read_excel(excel_file, sheet_name=None)
            
            frames = []
            for sheet_name, df in all_sheets.items():
                # Standardize columns for this sheet
                df.columns = [str(c).strip() for c in df.columns]
                frames.append(df)
            
            if not frames:
                 return Response({'error': 'No sheets found in the Google Excel file.'}, status=status.HTTP_400_BAD_REQUEST)

            # Combine all sheets
            df = pd.concat(frames, ignore_index=True)
            
            # Standardize names (again, for safety after concat)
            df.columns = [str(c).strip() for c in df.columns]
            
            # Map Google Sheet Columns to Model Fields
            # Found: ['S.NO', 'EMP CODE', 'NAME', 'GENDER', 'DEPT', 'DESIGNATION', 'DOJ', 'MOBILE NUMBER', 'KITE MAIL ID']
            
            required_cols = ['EMP CODE', 'NAME', 'DEPT']
            
            # Check if columns exist
            missing = [c for c in required_cols if c not in df.columns]
            if missing:
                 return Response({'error': f'Google Sheet missing columns: {missing}'}, status=status.HTTP_400_BAD_REQUEST)
            
            created_count = 0
            updated_count = 0
            
            excel_reg_nos = []
            
            for index, row in df.iterrows():
                # Map columns
                reg_no = str(row['EMP CODE']).strip()
                name = str(row['NAME']).strip()
                dept = str(row['DEPT']).strip()
                
                if not reg_no or pd.isna(row['EMP CODE']) or reg_no.lower() == 'nan':
                    continue
                
                # Handling integer conversion/cleanup for IDs if needed
                if reg_no.endswith('.0'):
                    reg_no = reg_no[:-2]
                    
                excel_reg_nos.append(reg_no)
                
                faculty, created = Faculty.objects.get_or_create(register_no=reg_no)
                
                if created:
                    faculty.name = name
                    faculty.department = dept
                    faculty.set_password('Kite@123')
                    faculty.save()
                    print(f"Created faculty: {name} ({reg_no})")
                    created_count += 1
                else:
                    if faculty.name != name or faculty.department != dept:
                        faculty.name = name
                        faculty.department = dept
                        faculty.save()
                        updated_count += 1
            
            # Sync deletes
            faculties_to_delete = Faculty.objects.exclude(register_no__in=excel_reg_nos)
            deleted_count = faculties_to_delete.count()
            faculties_to_delete.delete()
            
            return Response({
                'message': 'Sync successful',
                'stats': {
                    'created': created_count,
                    'updated': updated_count,
                    'deleted': deleted_count
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': f"Failed to sync from Google Sheet: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============ FACULTY SUBMODULE APIS ============

class FacultyDashboardView(APIView):
    """
    Returns today's invigilation duty for the logged-in faculty.
    """
    def get(self, request):
        token_key = request.headers.get('Authorization')
        if not token_key:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            key = token_key.replace('Token ', '').strip()
            token = FacultyToken.objects.get(key=key)
            if token.is_expired():
                token.delete()
                return Response(
                    {'error': 'Token expired'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            faculty = token.faculty
            # Use current date (UTC as per settings or local if needed)
            today = timezone.localtime(timezone.now()).date()
            
            from .models import FacultyAllocationStatus
            
            # Fetch all assignments for the faculty
            # Only show assignments where (date, session) is confirmed and faculty_active is True
            confirmed_status = FacultyAllocationStatus.objects.filter(is_confirmed=True, is_faculty_active=True)
            
            # This logic might be slow if there are many entries, but manageable for faculty duties.
            # Alternatively, join FacultyAllocation with FacultyAllocationStatus?
            # For now, let's filter allocations and then check status.
            
            duties = FacultyAllocation.objects.filter(
                faculty=faculty,
                is_confirmed=True
            ).order_by('exam_date', 'session')
            
            data = []
            from apps.exams.utils import resolve_hall_location
            
            for duty in duties:
                # Visibility Gate: Only show if the global toggle for this slot is ON
                is_active = FacultyAllocationStatus.objects.filter(
                    exam_date=duty.exam_date, 
                    session=duty.session,
                    is_faculty_active=True
                ).exists()
                
                if not is_active:
                    continue

                location = resolve_hall_location(duty.hall_no)
                
                # If duty is replaced, we show it as "Reassigned" without hall details
                item = {
                    'id': duty.id,
                    'session': duty.session,
                    'exam_date': duty.exam_date.strftime('%Y-%m-%d'),
                    'is_replaced': duty.is_replaced
                }
                
                if not duty.is_replaced:
                    item.update({
                        'hall_no': duty.hall_no,
                        'course_code': duty.course_code,
                        'course_title': duty.course_title,
                        'location': location,
                    })
                
                data.append(item)
                
            return Response(data)
            
        except FacultyToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


class FacultyStudentSeatingView(APIView):
    """
    Returns students assigned to the faculty's hall for today's session.
    """
    def get(self, request):
        token_key = request.headers.get('Authorization')
        hall_no = request.query_params.get('hall_no')
        session = request.query_params.get('session')
        date_str = request.query_params.get('date')
        
        if not token_key:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            key = token_key.replace('Token ', '').strip()
            token = FacultyToken.objects.get(key=key)
            faculty = token.faculty
            today = timezone.localtime(timezone.now()).date()
            
            # Verify assignment
            assignment_query = FacultyAllocation.objects.filter(
                faculty=faculty
            )
            if hall_no:
                assignment_query = assignment_query.filter(hall_no=hall_no)
            if session:
                assignment_query = assignment_query.filter(session=session)
            if date_str:
                try:
                    from datetime import datetime
                    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    assignment_query = assignment_query.filter(exam_date=target_date)
                except Exception:
                    pass
            
            # Order by latest exam date first so current allocations take precedence
            assignment = assignment_query.order_by('-exam_date').first()
            if not assignment:
                return Response(
                    {'error': 'No assignment found for this hall/session today.'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if assignment.is_replaced:
                return Response(
                    {'error': 'This assignment has been reassigned and is no longer accessible.'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            from apps.exams.models import Student, Dataset
            active_dataset = Dataset.objects.filter(is_active=True).first()
            if not active_dataset:
                active_dataset = Dataset.objects.order_by('-uploaded_at').first()
            students = Student.objects.filter(
                dataset=active_dataset,
                exam_date=assignment.exam_date,
                session=assignment.session,
                hall_no=assignment.hall_no
            ).order_by('seat_no')
            
            student_data = []
            from apps.exams.utils import get_department_from_register_no
            for s in students:
                # Clean seat number (remove .0 if it's a decimal from Excel)
                seat_no = str(s.seat_no).strip()
                try:
                    if '.' in seat_no:
                        seat_no = str(int(float(seat_no)))
                except:
                    pass

                student_data.append({
                    'register_no': s.register_no,
                    'name': s.name,
                    'department': get_department_from_register_no(s.register_no),
                    'seat_no': seat_no
                })
                
            from apps.exams.utils import resolve_hall_location
            return Response({
                'hall_no': assignment.hall_no,
                'location': resolve_hall_location(assignment.hall_no),
                'session': assignment.session,
                'course_code': assignment.course_code,
                'course_title': assignment.course_title,
                'students': student_data
            })
            
        except FacultyToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


class FacultyAllocationHistoryView(APIView):
    """
    Returns full history of invigilation for the logged-in faculty.
    """
    def get(self, request):
        token_key = request.headers.get('Authorization')
        if not token_key:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            key = token_key.replace('Token ', '').strip()
            token = FacultyToken.objects.get(key=key)
            faculty = token.faculty
            
            history = FacultyAllocation.objects.filter(faculty=faculty).order_by('-exam_date', '-session')
            
            from apps.exams.utils import resolve_hall_location
            data = []
            for h in history:
                data.append({
                    'date': h.exam_date.strftime('%Y-%m-%d'),
                    'hall': h.hall_no,
                    'location': resolve_hall_location(h.hall_no),
                    'session': h.session,
                    'course_code': h.course_code,
                    'course_title': h.course_title,
                    'status': 'Replaced' if h.is_replaced else 'Completed'
                })
            return Response(data)
            
        except FacultyToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


class FacultyAvailabilityUpdateView(APIView):
    """
    API for faculty to mark themselves as unavailable for a specific assignment.
    Input: { "allocation_id": 123, "reason": "Sick leave" }
    """
    def post(self, request):
        token_key = request.headers.get('Authorization')
        allocation_id = request.data.get('allocation_id')
        reason = request.data.get('reason')
        
        if not token_key:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not allocation_id or not reason:
            return Response(
                {'error': 'Missing allocation_id or reason'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            key = token_key.replace('Token ', '').strip()
            token = FacultyToken.objects.get(key=key)
            faculty = token.faculty
            
            # Verify the allocation belongs to this faculty
            try:
                allocation = FacultyAllocation.objects.get(id=allocation_id, faculty=faculty)
            except FacultyAllocation.DoesNotExist:
                return Response(
                    {'error': 'Allocation not found for this faculty'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
            from .utils import replace_faculty
            new_allocation = replace_faculty(allocation_id, reason)
            
            return Response({
                'message': 'Availability updated. Replacement assigned.',
                'replacement_faculty': new_allocation.faculty.name
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FacultyAlternationRequestView(APIView):
    """
    API for faculty members to submit an alternation request.
    """
    def post(self, request):
        token_key = request.headers.get('Authorization')
        if not token_key:
             return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
             
        try:
            key = token_key.replace('Token ', '').strip()
            token = FacultyToken.objects.get(key=key)
            faculty = token.faculty
            
            allocation_id = request.data.get('allocation_id')
            reason = request.data.get('reason')
            
            if not allocation_id or not reason:
                 return Response({'error': 'Allocation ID and reason are required'}, status=status.HTTP_400_BAD_REQUEST)
                 
            from .utils import request_alternation
            req_obj = request_alternation(faculty.register_no, allocation_id, reason)
            
            return Response({
                'message': 'Alternation request submitted successfully and is pending admin approval.',
                'request_id': req_obj.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminAlternationRequestListView(APIView):
    """
    API for admin to list faculty alternation requests.
    """
    def get(self, request):
        from .models import FacultyAlternationRequest
        status_filter = request.query_params.get('status', 'PENDING').upper()
        
        requests = FacultyAlternationRequest.objects.filter(status=status_filter).order_by('-created_at')
        
        data = []
        for r in requests:
            data.append({
                'id': r.id,
                'faculty_name': r.faculty.name,
                'faculty_reg_no': r.faculty.register_no,
                'department': r.faculty.department,
                'hall_no': r.allocation.hall_no,
                'exam_date': r.allocation.exam_date.strftime('%Y-%m-%d'),
                'session': r.allocation.session,
                'reason': r.reason,
                'status': r.status,
                'created_at': r.created_at.strftime('%Y-%m-%d %H:%M')
            })
        return Response(data)


class AdminAlternationApprovalView(APIView):
    """
    API for admin to approve or reject a faculty alternation request.
    """
    def post(self, request):
        request_id = request.data.get('request_id')
        action = request.data.get('action') # 'APPROVE' or 'REJECT'
        
        if not request_id or not action:
            return Response({'error': 'Request ID and action are required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            from .utils import approve_alternation, reject_alternation
            from django.contrib.auth.models import User
            # Simplified admin context for assignment
            admin_user = User.objects.filter(is_superuser=True).first()
            
            if action.upper() == 'APPROVE':
                approve_alternation(request_id, admin_user)
                return Response({'message': 'Request approved and faculty reassigned successfully.'})
            elif action.upper() == 'REJECT':
                reject_alternation(request_id, admin_user)
                return Response({'message': 'Request rejected.'})
            else:
                return Response({'error': 'Invalid action. Use APPROVE or REJECT.'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
