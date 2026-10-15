import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.exams.models import Dataset, Student

def print_samples():
    active = Dataset.objects.filter(is_active=True).first()
    if not active:
        print('No active dataset')
        return
    students = Student.objects.filter(dataset=active).order_by('id')[:200]
    print(f'Active dataset id={active.id}, total_students={students.count()} (showing up to 200)')
    for s in students:
        print(repr(s.register_no), '->', s.register_no)

if __name__ == '__main__':
    print_samples()
