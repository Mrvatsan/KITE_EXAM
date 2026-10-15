import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.exams.models import Dataset, Student

def status(registers=None):
    if registers is None:
        registers = ['2024001']

    print('Datasets:')
    for d in Dataset.objects.all().order_by('-uploaded_at'):
        print(f'  id={d.id} active={d.is_active} students={d.students.count()} uploaded_at={d.uploaded_at}')

    active = Dataset.objects.filter(is_active=True).first()
    print('\nActive dataset: ', active.id if active else None)

    for r in registers:
        print(f"\nChecking student register='{r}':")
        qs = Student.objects.filter(register_no=str(r))
        if not qs.exists():
            print('  Student not found (any dataset)')
        else:
            for s in qs:
                print(f"  id={s.id} dataset_id={s.dataset_id} dataset_active={s.dataset.is_active} name={s.name} password={s.password}")

if __name__ == '__main__':
    regs = sys.argv[1:] if len(sys.argv) > 1 else None
    status(registers=regs)
