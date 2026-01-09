
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.exams.models import Student, Dataset

active_dataset = Dataset.objects.filter(is_active=True).first()
if active_dataset:
    none_dates = Student.objects.filter(dataset=active_dataset, exam_date__isnull=True).count()
    total = Student.objects.filter(dataset=active_dataset).count()
    print(f"Total students in active dataset: {total}")
    print(f"Students with exam_date=None: {none_dates}")
    
    unique_dates = Student.objects.filter(dataset=active_dataset).values_list('exam_date', flat=True).distinct()
    print(f"Unique dates: {list(unique_dates)}")
else:
    print("No active dataset.")
