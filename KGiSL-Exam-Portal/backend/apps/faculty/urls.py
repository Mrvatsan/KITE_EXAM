from django.urls import path
from .views import (
    FacultyLoginView, FacultyLogoutView, FacultyProfileView,
    AdminFacultyAllocationView, AdminFacultyListView,
    AdminFacultyConfirmView,
    FacultyDashboardView, FacultyStudentSeatingView, FacultyAllocationHistoryView,
    FacultyAvailabilityUpdateView
)

urlpatterns = [
    path('login/', FacultyLoginView.as_view(), name='faculty-login'),
    path('logout/', FacultyLogoutView.as_view(), name='faculty-logout'),
    path('profile/', FacultyProfileView.as_view(), name='faculty-profile'),
    path('admin/allocate/', AdminFacultyAllocationView.as_view(), name='faculty-admin-allocate'),
    path('admin/list/', AdminFacultyListView.as_view(), name='faculty-admin-list'),
    path('admin/confirm/', AdminFacultyConfirmView.as_view(), name='faculty-admin-confirm'),
    path('dashboard/', FacultyDashboardView.as_view(), name='faculty-dashboard'),
    path('students/', FacultyStudentSeatingView.as_view(), name='faculty-students'),
    path('history/', FacultyAllocationHistoryView.as_view(), name='faculty-history'),
    path('availability/update/', FacultyAvailabilityUpdateView.as_view(), name='faculty-availability-update'),
]
