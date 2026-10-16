import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from django.contrib.auth.models import User
user = User.objects.filter(username__iexact='Kgkite').first()
if not user:
    User.objects.create_superuser('Kgkite', 'admin@example.com', 'Kgkite@123')
    print("Superuser 'Kgkite' created.")
else:
    user.set_password('Kgkite@123')
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.save()
    print("Superuser 'Kgkite' password and permissions updated.")
