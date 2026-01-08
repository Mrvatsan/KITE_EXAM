import os
import django
import sys
import unittest
from unittest.mock import patch, MagicMock

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.faculty.models import Faculty, FacultyAllocation, FacultyRotationState, FacultyAllocationStatus
from apps.exams.models import Student, Dataset
from apps.faculty.utils import run_faculty_allocation, confirm_faculty_allocation
from datetime import date

class TestFacultyAllocation(unittest.TestCase):
    def setUp(self):
        # Clear existing data
        FacultyAllocation.objects.all().delete()
        FacultyAllocationStatus.objects.all().delete()
        FacultyRotationState.objects.all().delete()
        Faculty.objects.all().delete()
        Student.objects.all().delete()
        Dataset.objects.all().delete()

        # Create active dataset
        self.dataset = Dataset.objects.create(is_active=True)
        
        # Create test halls
        self.halls = ['H101', 'H102']
        for hall in self.halls:
            Student.objects.create(
                dataset=self.dataset,
                register_no=f"REG_{hall}",
                name=f"Student {hall}",
                hall_no=hall,
                exam_date=date(2026, 1, 10),
                session='FN',
                course_code='C101',
                course_title='Test Course',
                seat_no=1
            )

    @patch('apps.faculty.utils.get_faculty_sheet_data')
    def test_allocation_preview_flow(self, mock_sheet_data):
        # Mock faculty data
        import pandas as pd
        mock_df = pd.DataFrame([
            {'register_no': 'F1', 'name': 'Professor A', 'department': 'CSE', 'designation': 'Professor'},
            {'register_no': 'F2', 'name': 'Professor B', 'department': 'CSE', 'designation': 'Professor'},
            {'register_no': 'F3', 'name': 'Assistant A', 'department': 'CSE', 'designation': 'Assistant Professor'},
        ])
        mock_sheet_data.return_value = mock_df

        dept_counts = {'CSE': 2}
        test_date = date(2026, 1, 10)
        test_session = 'FN'

        # 1. Run Preview
        run_faculty_allocation(dept_counts, test_date, test_session, 'Professor')
        
        allocations = FacultyAllocation.objects.filter(exam_date=test_date, session=test_session)
        self.assertEqual(allocations.count(), 2)
        self.assertFalse(allocations.filter(is_confirmed=True).exists())
        
        # Check rotation state (should NOT be updated yet)
        state = FacultyRotationState.objects.get(department='CSE', designation='Professor')
        self.assertEqual(state.last_row_index, -1)

        # 2. Confirm
        confirm_faculty_allocation(test_date, test_session)
        
        # Check confirmation
        allocations = FacultyAllocation.objects.filter(exam_date=test_date, session=test_session)
        self.assertTrue(all(a.is_confirmed for a in allocations))
        
        status = FacultyAllocationStatus.objects.get(exam_date=test_date, session=test_session)
        self.assertTrue(status.is_confirmed)

        # Check rotation state (should be updated now)
        # Sequence: start from bottom (idx 1). Pick F2 then F1? 
        # Actually our logic for -1 starts from (total-count)%total. (2-2)%2 = 0.
        # Indices [0, 1] i.e. F1, F2. Max idx is 1.
        state.refresh_from_db()
        self.assertEqual(state.last_row_index, 1)

    @patch('apps.faculty.utils.get_faculty_sheet_data')
    def test_visibility_toggle(self, mock_sheet_data):
         # Logic for FacultyDashboardView
         status_obj = FacultyAllocationStatus.objects.create(
             exam_date=date(2026, 1, 10),
             session='FN',
             is_confirmed=True,
             is_faculty_active=False
         )
         
         # Verification of dashboard logic (simulated)
         # In views.py: status_obj = FacultyAllocationStatus.objects.filter(..., is_faculty_active=True).exists()
         self.assertFalse(FacultyAllocationStatus.objects.filter(
             exam_date=date(2026, 1, 10), 
             session='FN', 
             is_faculty_active=True
         ).exists())
         
         status_obj.is_faculty_active = True
         status_obj.save()
         
         self.assertTrue(FacultyAllocationStatus.objects.filter(
             exam_date=date(2026, 1, 10), 
             session='FN', 
             is_faculty_active=True
         ).exists())

if __name__ == '__main__':
    unittest.main()
