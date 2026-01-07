from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Faculty, FacultyToken
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
