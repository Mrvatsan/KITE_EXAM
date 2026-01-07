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
        register_no = request.data.get('register_no')
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
        
        if not dept_counts or not date_str or not session:
            return Response(
                {'error': 'Missing required fields: dept_counts, date, session'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            from .utils import run_faculty_allocation
            allocations = run_faculty_allocation(dept_counts, date_obj, session)
            
            data = []
            for alloc in allocations:
                data.append({
                    'hall_no': alloc.hall_no,
                    'faculty_name': alloc.faculty.name,
                    'faculty_reg_no': alloc.faculty.register_no,
                    'department': alloc.faculty.department,
                    'course_code': alloc.course_code,
                    'course_title': alloc.course_title
                })
                
            return Response({
                'message': 'Allocation completed successfully',
                'allocations': data
            }, status=status.HTTP_200_OK)
            
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
            ).order_by('hall_no')
            
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
                    'is_replaced': alloc.is_replaced
                })
            return Response(data)
        except Exception as e:
             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
            
            duties = FacultyAllocation.objects.filter(faculty=faculty, exam_date=today)
            
            from apps.exams.utils import get_block_from_hall_no, get_floor_from_hall_no
            
            data = []
            for duty in duties:
                block = get_block_from_hall_no(duty.hall_no)
                floor = get_floor_from_hall_no(duty.hall_no, block=block)
                
                data.append({
                    'id': duty.id,
                    'hall_no': duty.hall_no,
                    'course_code': duty.course_code,
                    'course_title': duty.course_title,
                    'session': duty.session,
                    'exam_date': duty.exam_date.strftime('%Y-%m-%d'),
                    'block': block,
                    'floor': floor,
                    'is_replaced': duty.is_replaced
                })
                
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
                faculty=faculty, 
                exam_date=today
            )
            if hall_no:
                assignment_query = assignment_query.filter(hall_no=hall_no)
            if session:
                assignment_query = assignment_query.filter(session=session)
            
            assignment = assignment_query.first()
            if not assignment:
                return Response(
                    {'error': 'No assignment found for this hall/session today.'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            from apps.exams.models import Student, Dataset
            active_dataset = Dataset.objects.filter(is_active=True).first()
            students = Student.objects.filter(
                dataset=active_dataset,
                exam_date=today,
                session=assignment.session,
                hall_no=assignment.hall_no
            ).order_by('seat_no')
            
            student_data = []
            from apps.exams.utils import get_department_from_register_no
            for s in students:
                student_data.append({
                    'register_no': s.register_no,
                    'name': s.name,
                    'department': get_department_from_register_no(s.register_no),
                    'seat_no': s.seat_no
                })
                
            return Response({
                'hall_no': assignment.hall_no,
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
            
            data = []
            for h in history:
                data.append({
                    'date': h.exam_date.strftime('%Y-%m-%d'),
                    'hall': h.hall_no,
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
