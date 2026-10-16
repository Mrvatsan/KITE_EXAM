import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

User = get_user_model()

# Superuser credentials to ensure exist on Render and local environments
SUPERUSERS = [
    {
        'username': 'Kgkite',
        'email': 'admin@example.com',
        'password': 'Kgkite@123',
    },
    {
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'admin123',
    },
]

# Allow overriding or adding from environment variables if set
env_user = os.environ.get('DJANGO_SUPERUSER_USERNAME')
env_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
env_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if env_user and env_password:
    matched = False
    for cred in SUPERUSERS:
        if cred['username'].lower() == env_user.lower():
            cred['password'] = env_password
            cred['email'] = env_email
            matched = True
            break
    if not matched:
        SUPERUSERS.insert(0, {
            'username': env_user,
            'email': env_email,
            'password': env_password,
        })

print("Ensuring admin superuser accounts are configured...")
for cred in SUPERUSERS:
    username = cred['username']
    password = cred['password']
    email = cred['email']
    try:
        user = User.objects.filter(username__iexact=username).first()
        if not user:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"Created new superuser: '{username}'")
        else:
            user.set_password(password)
            user.email = email
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            print(f"Updated existing superuser: '{user.username}' (password synced)")
    except Exception as exc:
        print(f"Notice: Failed to create or update superuser '{username}': {exc}")

print("Superuser provisioning complete.")
