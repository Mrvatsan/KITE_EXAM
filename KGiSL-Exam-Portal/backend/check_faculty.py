import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.faculty.models import Faculty, FacultyAllocation, FacultyAllocationStatus
from django.db.models import Count

print("=" * 60)
print("FACULTY DATASET CHECK")
print("=" * 60)

total_faculty = Faculty.objects.count()
print(f"\nTotal Faculty Members: {total_faculty}")

if total_faculty == 0:
    print("\n⚠️ WARNING: No faculty members found in database!")
    print("This will cause allocation to fail.")
else:
    print("\nFaculty by Department:")
    print("-" * 40)
    for dept in Faculty.objects.values('department').annotate(count=Count('id')).order_by('department'):
        print(f"  {dept['department']}: {dept['count']} faculty members")

print("\n" + "=" * 60)
print("ALLOCATION STATUS CHECK")
print("=" * 60)

allocations = FacultyAllocation.objects.all()
print(f"\nTotal Allocations: {allocations.count()}")

if allocations.count() > 0:
    print("\nAllocations by Date and Session:")
    print("-" * 40)
    for alloc in FacultyAllocation.objects.values('exam_date', 'session').annotate(count=Count('id')).order_by('exam_date', 'session'):
        print(f"  {alloc['exam_date']} ({alloc['session']}): {alloc['count']} allocations")

print("\n" + "=" * 60)
print("ALLOCATION STATUS RECORDS")
print("=" * 60)

statuses = FacultyAllocationStatus.objects.all()
print(f"\nTotal Status Records: {statuses.count()}")

if statuses.count() > 0:
    print("\nStatus Details:")
    print("-" * 40)
    for status in statuses:
        print(f"  Date: {status.exam_date}, Session: {status.session}")
        print(f"    Confirmed: {status.is_confirmed}")
        print(f"    Active: {status.is_faculty_active}")
        print()
