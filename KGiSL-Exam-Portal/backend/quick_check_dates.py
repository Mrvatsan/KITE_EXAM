import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.exams.models import Student, Dataset

active = Dataset.objects.filter(is_active=True).first()
if active:
    print('Active Dataset:', active.uploaded_at)
    print('\nAvailable Exam Dates in Dataset:')
    dates = Student.objects.filter(dataset=active).values('exam_date', 'session').distinct().order_by('exam_date')
    for d in dates:
        halls = Student.objects.filter(dataset=active, exam_date=d['exam_date'], session=d['session']).values('hall_no').distinct().count()
        print(f"  {d['exam_date']} - {d['session']} ({halls} halls)")
else:
    print('No active dataset found!')
