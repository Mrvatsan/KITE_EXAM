import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(username, email, password, is_staff=False, is_superuser=False):
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        print(f"Created user: {username}")
    else:
        print(f"User already exists: {username}")

if __name__ == '__main__':
    create_user('admin', 'admin@example.com', 'AdminPass123!')
    # ensure admin has the desired password and flags
    u = User.objects.get(username='admin')
    u.set_password('AdminPass123!')
    u.is_staff = True
    u.is_superuser = True
    u.save()

    create_user('faculty', 'faculty@example.com', 'FacultyPass123!')
    f = User.objects.get(username='faculty')
    f.set_password('FacultyPass123!')
    f.save()

    create_user('student', 'student@example.com', 'StudentPass123!')
    s = User.objects.get(username='student')
    s.set_password('StudentPass123!')
    s.save()
