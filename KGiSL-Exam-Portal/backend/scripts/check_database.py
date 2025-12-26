import django
django.setup()

from exams.models import HallTicketExam

# Check database contents
count = HallTicketExam.objects.count()
print(f'\nTotal hall ticket records in database: {count}')

if count > 0:
    depts = HallTicketExam.objects.values_list('department', flat=True).distinct()
    print(f'Departments in database: {list(depts)}')
    
    sample = HallTicketExam.objects.first()
    print(f'\nSample record:')
    print(f'  Department: {sample.department}')
    print(f'  Semester: {sample.semester}')
    print(f'  Course: {sample.course_code}')
else:
    print('\nDatabase is EMPTY - Excel file has not been loaded yet!')
    print('The Excel file will be auto-loaded on first hall ticket request.')
