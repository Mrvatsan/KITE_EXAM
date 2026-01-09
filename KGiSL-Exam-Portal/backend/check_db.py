
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.exams.models import Student, Dataset
from apps.faculty.models import FacultyAllocation

print("Active Datasets:")
for d in Dataset.objects.filter(is_active=True):
    print(f"ID: {d.id}, Uploaded: {d.uploaded_at}")

print("\nStudent Exam Dates and Sessions in active dataset:")
active_dataset = Dataset.objects.filter(is_active=True).first()
if active_dataset:
    dates_sessions = Student.objects.filter(dataset=active_dataset).values('exam_date', 'session').distinct()
    for ds in dates_sessions:
        print(f"Date: {ds['exam_date']}, Session: {ds['session']}")
else:
    print("No active dataset.")

print("\nFaculty Allocations:")
for fa in FacultyAllocation.objects.all():
    print(f"ID: {fa.id}, Faculty: {fa.faculty.name}, Date: {fa.exam_date}, Session: {fa.session}, Hall: {fa.hall_no}")
