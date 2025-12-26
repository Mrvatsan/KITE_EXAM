import os
import sys
sys.path.insert(0, 'd:/studentadmin')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from exams.models import Student, Dataset

# Get active dataset
active_dataset = Dataset.objects.filter(is_active=True).first()

if active_dataset:
    print(f'Active Dataset ID: {active_dataset.id}')
    print(f'Uploaded at: {active_dataset.uploaded_at}')
    print()
    
    # Get sample students
    students = Student.objects.filter(dataset=active_dataset)[:5]
    
    print('Sample student exam dates from database:')
    print('=' * 70)
    for s in students:
        print(f'Register: {s.register_no}')
        print(f'  Name: {s.name}')
        print(f'  Exam Date (raw): {s.exam_date}')
        print(f'  Exam Date (type): {type(s.exam_date)}')
        if s.exam_date:
            print(f'  Exam Date (formatted): {s.exam_date.strftime("%Y-%m-%d")}')
            print(f'  Exam Date (display format): {s.exam_date.strftime("%d-%m-%Y")}')
        print()
else:
    print('No active dataset found!')
