import os
import sys

# Add the project to path
sys.path.insert(0, 'd:/studentadmin')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from exams.models import HallTicketExam
from exams.utils import parse_hall_ticket_excel

# Path to Excel file
excel_path = 'd:/studentadmin/HALL_TICKET.xlsx'

print(f'Loading Excel file: {excel_path}')
print(f'File exists: {os.path.exists(excel_path)}')

if os.path.exists(excel_path):
    with open(excel_path, 'rb') as excel_file:
        print('\nParsing Excel file...')
        records = parse_hall_ticket_excel(excel_file)
        
        print(f'\nParsed {len(records)} records')
        
        if records:
            print('\nSample records:')
            for i, record in enumerate(records[:5]):
                print(f'  {i+1}. Dept: {record["department"]}, Sem: {record["semester"]}, Course: {record["course_code"]}')
            
            print('\nClearing existing data...')
            HallTicketExam.objects.all().delete()
            
            print('Inserting records into database...')
            exam_objects = [HallTicketExam(**record) for record in records]
            HallTicketExam.objects.bulk_create(exam_objects)
            
            print(f'\n✓ Successfully loaded {len(records)} records into database')
            
            # Verify
            count = HallTicketExam.objects.count()
            depts = list(HallTicketExam.objects.values_list('department', flat=True).distinct())
            print(f'\nDatabase verification:')
            print(f'  Total records: {count}')
            print(f'  Departments: {depts}')
        else:
            print('\n✗ No records parsed from Excel file!')
else:
    print('\n✗ Excel file not found!')
