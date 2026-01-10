import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.exams.models import Student, Dataset
from datetime import datetime

print("=" * 60)
print("AVAILABLE EXAM DATES IN DATASET")
print("=" * 60)

active_dataset = Dataset.objects.filter(is_active=True).first()

if not active_dataset:
    print("\n⚠️ WARNING: No active dataset found!")
    print("Please upload and activate a student dataset first.")
else:
    print(f"\nActive Dataset: Uploaded on {active_dataset.uploaded_at}")
    print(f"Total Students: {Student.objects.filter(dataset=active_dataset).count()}")
    
    print("\n" + "-" * 60)
    print("Available Exam Dates and Sessions:")
    print("-" * 60)
    
    dates_sessions = Student.objects.filter(dataset=active_dataset).values('exam_date', 'session').distinct().order_by('exam_date', 'session')
    
    if dates_sessions.count() == 0:
        print("\n⚠️ No exam dates found in active dataset!")
    else:
        for ds in dates_sessions:
            count = Student.objects.filter(dataset=active_dataset, exam_date=ds['exam_date'], session=ds['session']).count()
            halls = Student.objects.filter(dataset=active_dataset, exam_date=ds['exam_date'], session=ds['session']).values('hall_no').distinct().count()
            print(f"\n  📅 Date: {ds['exam_date']} | Session: {ds['session']}")
            print(f"     Students: {count} | Halls: {halls}")

print("\n" + "=" * 60)
