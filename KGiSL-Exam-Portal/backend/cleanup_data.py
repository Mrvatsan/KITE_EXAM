
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.exams.models import Student

for student in Student.objects.all():
    updated = False
    hall_no = str(student.hall_no).strip()
    seat_no = str(student.seat_no).strip()
    
    if '.' in hall_no:
        try:
            student.hall_no = str(int(float(hall_no)))
            updated = True
        except:
            pass
            
    if '.' in seat_no:
        try:
            student.seat_no = str(int(float(seat_no)))
            updated = True
        except:
            pass
            
    if updated:
        student.save()
        print(f"Cleaned Student {student.register_no}: Hall {student.hall_no}, Seat {student.seat_no}")

print("Cleanup complete.")
