from django.urls import path
from .views import (
    FacultyLoginView, FacultyLogoutView, FacultyProfileView,
    AdminFacultyAllocationView, AdminFacultyListView,
    AdminFacultyConfirmView, AdminFacultyStatusView,
    AdminFacultyListCreateView, AdminFacultyDetailView,
    OpenFacultyExcelView, SyncFacultyExcelView,
    FacultyDashboardView, FacultyStudentSeatingView, FacultyAllocationHistoryView,
    FacultyAvailabilityUpdateView,
    FacultyAlternationRequestView, AdminAlternationRequestListView, AdminAlternationApprovalView
)

urlpatterns = [
    path('login/', FacultyLoginView.as_view(), name='faculty-login'),
    path('logout/', FacultyLogoutView.as_view(), name='faculty-logout'),
    path('profile/', FacultyProfileView.as_view(), name='faculty-profile'),
    path('admin/allocate/', AdminFacultyAllocationView.as_view(), name='faculty-admin-allocate'),
    path('admin/list/', AdminFacultyListView.as_view(), name='faculty-admin-list'),
    path('admin/confirm/', AdminFacultyConfirmView.as_view(), name='faculty-admin-confirm'),
    path('admin/status/', AdminFacultyStatusView.as_view(), name='faculty-admin-status'),
    path('admin/data/', AdminFacultyListCreateView.as_view(), name='faculty-admin-list-create'),
    path('admin/data/<int:pk>/', AdminFacultyDetailView.as_view(), name='faculty-admin-detail'),
    path('admin/open-excel/', OpenFacultyExcelView.as_view(), name='faculty-admin-open-excel'),
    path('admin/sync-excel/', SyncFacultyExcelView.as_view(), name='faculty-admin-sync-excel'),
    path('dashboard/', FacultyDashboardView.as_view(), name='faculty-dashboard'),
    path('students/', FacultyStudentSeatingView.as_view(), name='faculty-students'),
    path('history/', FacultyAllocationHistoryView.as_view(), name='faculty-history'),
    path('availability/update/', FacultyAvailabilityUpdateView.as_view(), name='faculty-availability-update'),
    path('alternation/request/', FacultyAlternationRequestView.as_view(), name='faculty-alternation-request'),
    path('admin/alternation/requests/', AdminAlternationRequestListView.as_view(), name='admin-alternation-requests'),
    path('admin/alternation/approve/', AdminAlternationApprovalView.as_view(), name='admin-alternation-approve'),
]
