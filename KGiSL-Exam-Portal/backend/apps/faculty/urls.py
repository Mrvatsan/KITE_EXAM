from django.urls import path
from .views import FacultyLoginView, FacultyLogoutView, FacultyProfileView

urlpatterns = [
    path('login/', FacultyLoginView.as_view(), name='faculty-login'),
    path('logout/', FacultyLogoutView.as_view(), name='faculty-logout'),
    path('profile/', FacultyProfileView.as_view(), name='faculty-profile'),
]
