from django.urls import path
from .views import (
    LoginView, DatasetUploadView, DatasetListView, 
    ToggleDatasetView, DeleteStudentsView,
    HallTicketView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('upload/', DatasetUploadView.as_view(), name='upload'),
    path('datasets/', DatasetListView.as_view(), name='datasets'),
    path('datasets/<int:pk>/toggle/', ToggleDatasetView.as_view(), name='toggle-dataset'),
    path('delete-all/', DeleteStudentsView.as_view(), name='delete-all'),
    
    # Hall Ticket endpoint (student-only)
    path('hall-ticket/', HallTicketView.as_view(), name='hall-ticket'),
]
