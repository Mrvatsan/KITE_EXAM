import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.faculty.models import Faculty
from django.conf import settings

def generate_excel():
    print("Fetching faculty data...")
    faculty_list = Faculty.objects.all().order_by('department', 'register_no')
    
    data = []
    for f in faculty_list:
        data.append({
            'Register No': f.register_no,
            'Name': f.name,
            'Department': f.department,
            'Designation': 'Assistant Professor' # Defaulting as per model limitations, or fetch if added
        })
    
    if not data:
        print("No faculty found in database.")
        return

    df = pd.DataFrame(data)
    
    # Ensure media directory exists
    media_path = settings.MEDIA_ROOT
    if not os.path.exists(media_path):
        os.makedirs(media_path)
        
    file_path = os.path.join(media_path, 'Faculty.xlsx')
    
    print(f"Generating Excel file at: {file_path}")
    df.to_excel(file_path, index=False)
    print("✓ Faculty.xlsx generated successfully.")

if __name__ == '__main__':
    generate_excel()
