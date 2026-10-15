import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.exams.models import Student

def clean_reg(r):
    if r is None:
        return ''
    s = str(r).strip()
    if s.endswith('.0') and s.replace('.0','').isdigit():
        s = s[:-2]
    # If it's a float string like '2024001.000' remove decimals
    if '.' in s:
        try:
            f = float(s)
            if f.is_integer():
                s = str(int(f))
        except Exception:
            pass
    return s

def main():
    changed = 0
    for s in Student.objects.all():
        orig = s.register_no
        new = clean_reg(orig)
        if new != (orig or ''):
            s.register_no = new
            changed += 1
        # Ensure password exists and is not NULL/empty
        if not s.password:
            s.password = 'Kite@12345'
            changed += 1
        s.save()

    print(f"Normalized students. Changes: {changed}")

if __name__ == '__main__':
    main()
