import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='Kgkite').exists():
    User.objects.create_superuser('Kgkite', 'admin@example.com', 'Kgkite@123')
    print("Superuser 'Kgkite' created.")
else:
    print("Superuser 'Kgkite' already exists.")
