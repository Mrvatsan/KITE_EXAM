
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.exams.models import Student, Dataset

active_dataset = Dataset.objects.filter(is_active=True).first()
if active_dataset:
    empty_halls = Student.objects.filter(dataset=active_dataset, hall_no='').count()
    null_halls = Student.objects.filter(dataset=active_dataset, hall_no__isnull=True).count()
    all_halls = list(Student.objects.filter(dataset=active_dataset).values_list('hall_no', flat=True).distinct())
    print(f"Empty halls: {empty_halls}")
    print(f"Null halls: {null_halls}")
    print(f"All halls: {all_halls}")
else:
    print("No active dataset.")
