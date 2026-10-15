import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Ensure Django settings are loaded for model imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from apps.faculty.utils import get_faculty_sheet_data

try:
    df = get_faculty_sheet_data('COMPUTER SCIENCE ENGINEERING')
    print('Loaded sheet with columns:', df.columns.tolist())
    print(df.head().to_string())
except Exception as e:
    print('ERROR:', e)
