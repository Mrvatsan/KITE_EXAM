import os
import sys
sys.path.insert(0, 'd:/studentadmin')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from exams.models import Student, Dataset
from exams.utils import clean_and_parse_excel
import pandas as pd
from datetime import datetime

# Get the active dataset
active_dataset = Dataset.objects.filter(is_active=True).first()

if not active_dataset:
    print('No active dataset found!')
    exit(1)

print(f'Active Dataset ID: {active_dataset.id}')
print(f'File: {active_dataset.file.path}')

# Re-parse the file with correct date handling
with open(active_dataset.file.path, 'rb') as f:
    df = clean_and_parse_excel(f)

print(f'\nParsed {len(df)} rows from Excel')

# Delete existing students for this dataset
Student.objects.filter(dataset=active_dataset).delete()
print('Deleted old student records')

# Re-create students with correct dates
students_to_create = []
for _, row in df.iterrows():
    e_date = row.get('exam_date')
    parsed_date = None
    
    if pd.notna(e_date):
        try:
            # Try string date format first (YYYY-MM-DD)
            if isinstance(e_date, str):
                parsed_date = datetime.strptime(e_date, '%Y-%m-%d').date()
            else:
                # Try pandas datetime
                parsed_date = pd.to_datetime(e_date, errors='coerce').date()
                
                # If still None, try Excel serial number
                if parsed_date is None or str(parsed_date) == 'NaT':
                    from datetime import timedelta
                    if isinstance(e_date, (int, float)) and e_date > 0:
                        excel_epoch = datetime(1899, 12, 30)
                        parsed_date = (excel_epoch + timedelta(days=float(e_date))).date()
        except Exception as e:
            print(f'Date parsing error for {e_date}: {e}')
            parsed_date = None
    
    students_to_create.append(Student(
        dataset=active_dataset,
        register_no=row.get('register_no', ''),
        name=row.get('name', ''),
        course_code=row.get('course_code', ''),
        course_title=row.get('course_title', ''),
        exam_date=parsed_date,
        session=row.get('session', ''),
        hall_no=str(row.get('hall_no', '')),
        seat_no=str(row.get('seat_no', '')),
        password='Kite@12345'
    ))

Student.objects.bulk_create(students_to_create)
print(f'\nCreated {len(students_to_create)} student records')

# Verify
sample = Student.objects.filter(dataset=active_dataset).first()
print(f'\nSample student:')
print(f'  Name: {sample.name}')
print(f'  Exam Date: {sample.exam_date}')
print(f'  Hall No: {sample.hall_no}')
print(f'  Seat No: {sample.seat_no}')

print('\n✓ Data reloaded successfully!')
