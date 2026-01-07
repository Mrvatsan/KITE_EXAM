from .views import (
    FacultyLoginView, FacultyLogoutView, FacultyProfileView,
    AdminFacultyAllocationView, AdminFacultyListView
)

urlpatterns = [
    path('login/', FacultyLoginView.as_view(), name='faculty-login'),
    path('logout/', FacultyLogoutView.as_view(), name='faculty-logout'),
    path('profile/', FacultyProfileView.as_view(), name='faculty-profile'),
    path('admin/allocate/', AdminFacultyAllocationView.as_view(), name='faculty-admin-allocate'),
    path('admin/list/', AdminFacultyListView.as_view(), name='faculty-admin-list'),
]
