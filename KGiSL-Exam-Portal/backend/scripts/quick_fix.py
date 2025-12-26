import os, sys
sys.path.insert(0, 'd:/studentadmin')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from exams.models import Student, Dataset
import pandas as pd
from datetime import datetime

active_dataset = Dataset.objects.filter(is_active=True).first()
print(f'Reloading data for dataset {active_dataset.id}')

# Read Excel directly
df = pd.read_excel(active_dataset.file.path, engine='openpyxl')
print(f'Read {len(df)} rows')

# Delete old data
Student.objects.filter(dataset=active_dataset).delete()

# Create new students with CORRECT date parsing
students = []
for _, row in df.iterrows():
    e_date_str = str(row['ExamDate']).strip()  # Get as string
    try:
        exam_date = datetime.strptime(e_date_str, '%Y-%m-%d').date()
    except:
        exam_date = None
    
    # Clean hall/seat numbers
    hall_no = str(row['ExamHallNumber']).strip()
    seat_no = str(row['ExamSeatNumber']).strip()
    if '.' in hall_no:
        hall_no = str(int(float(hall_no)))
    if '.' in seat_no:
        seat_no = str(int(float(seat_no)))
    
    students.append(Student(
        dataset=active_dataset,
        register_no=str(row['Registerno']).strip(),
        name=str(row['StudentName']).strip(),
        course_code=str(row['Coursecode']).strip(),
        course_title=str(row['CourseTitle']).strip(),
        exam_date=exam_date,
        session=str(row['ExamSession']).strip(),
        hall_no=hall_no,
        seat_no=seat_no,
        password='Kite@12345'
    ))

Student.objects.bulk_create(students)
print(f'Created {len(students)} students')

# Verify
s = Student.objects.first()
print(f'\nVerification:')
print(f'Name: {s.name}')
print(f'Exam Date: {s.exam_date}')
print(f'Hall No: {s.hall_no}')
print(f'Seat No: {s.seat_no}')
