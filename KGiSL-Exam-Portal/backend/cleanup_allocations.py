
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.faculty.models import FacultyAllocation

for alloc in FacultyAllocation.objects.all():
    hall_no = str(alloc.hall_no).strip()
    if '.' in hall_no:
        try:
            alloc.hall_no = str(int(float(hall_no)))
            alloc.save()
            print(f"Cleaned Allocation {alloc.id}: Hall {alloc.hall_no}")
        except:
            pass

print("Cleanup complete.")
