import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.exams.models import Dataset, Student

def create():
    ds, created = Dataset.objects.get_or_create(is_active=True)
    if created:
        print(f"Created Dataset {ds.id}")
    else:
        print(f"Using existing Dataset {ds.id}")

    # Create student record expected by the verification scripts
    reg_no = '2024001'
    student, screated = Student.objects.get_or_create(
        dataset=ds,
        register_no=reg_no,
        defaults={
            'name': 'Test Student',
            'course_code': 'C101',
            'course_title': 'Test Course',
            'exam_date': date(2026,1,10),
            'session': 'FN',
            'hall_no': 'H101',
            'seat_no': 'A1',
            'password': 'password123'
        }
    )
    if screated:
        print(f"Created Student {reg_no}")
    else:
        student.password = 'password123'
        student.save()
        print(f"Ensured Student {reg_no} exists and password set")

if __name__ == '__main__':
    create()
