import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
import django
django.setup()
from apps.exams.utils import normalize_department_name
print('COMPUTER SCIENCE ENGINEERING ->', normalize_department_name('COMPUTER SCIENCE ENGINEERING'))
print('CSE ->', normalize_department_name('CSE'))
print('COMPUTER SCIENCE AND ENGINEERING ->', normalize_department_name('COMPUTER SCIENCE AND ENGINEERING'))
