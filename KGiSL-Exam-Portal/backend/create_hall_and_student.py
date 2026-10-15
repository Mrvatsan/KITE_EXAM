import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.exams.models import Dataset, Student, HallTicketExam

def create():
    ds, _ = Dataset.objects.get_or_create(is_active=True)

    reg = '711623UCS089'
    student, screated = Student.objects.get_or_create(
        dataset=ds,
        register_no=reg,
        defaults={
            'name': 'Dept Student',
            'course_code': 'C200',
            'course_title': 'Dept Course',
            'exam_date': date(2026,1,10),
            'session': 'FN',
            'hall_no': '101',
            'seat_no': '10',
            'password': 'deptpass'
        }
    )
    if screated:
        print(f"Created student {reg}")
    else:
        print(f"Using existing student {reg}")

    # Create a simple hall ticket exam record for CSE
    exam, ecreated = HallTicketExam.objects.get_or_create(
        department='CSE',
        semester='III',
        course_code='C200',
        course_title='Dept Course',
        exam_date=date(2026,1,15),
        session='FN'
    )
    if ecreated:
        print("Created HallTicketExam for CSE")
    else:
        print("Using existing HallTicketExam for CSE")

if __name__ == '__main__':
    create()
