import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.faculty.models import Faculty

# Define faculty members for each department
faculty_data = [
    # CSE Department - Assistant Professors
    {"name": "Dr. Rajesh Kumar", "register_no": "CSE001", "department": "CSE", "designation": "Assistant Professor"},
    {"name": "Dr. Priya Sharma", "register_no": "CSE002", "department": "CSE", "designation": "Assistant Professor"},
    {"name": "Dr. Amit Patel", "register_no": "CSE003", "department": "CSE", "designation": "Assistant Professor"},
    {"name": "Dr. Sneha Reddy", "register_no": "CSE004", "department": "CSE", "designation": "Assistant Professor"},
    {"name": "Dr. Vikram Singh", "register_no": "CSE005", "department": "CSE", "designation": "Assistant Professor"},
    
    # CSE Department - Associate Professors
    {"name": "Dr. Meera Iyer", "register_no": "CSE006", "department": "CSE", "designation": "Associate Professor"},
    {"name": "Dr. Arun Kapoor", "register_no": "CSE007", "department": "CSE", "designation": "Associate Professor"},
    {"name": "Dr. Kavita Nair", "register_no": "CSE008", "department": "CSE", "designation": "Associate Professor"},
    
    # AI&ML Department
    {"name": "Dr. Deepak Verma", "register_no": "AIML001", "department": "AI&ML", "designation": "Assistant Professor"},
    {"name": "Dr. Ananya Roy", "register_no": "AIML002", "department": "AI&ML", "designation": "Assistant Professor"},
    {"name": "Dr. Rahul Mehta", "register_no": "AIML003", "department": "AI&ML", "designation": "Assistant Professor"},
    {"name": "Dr. Pooja Gupta", "register_no": "AIML004", "department": "AI&ML", "designation": "Associate Professor"},
    {"name": "Dr. Sanjay Joshi", "register_no": "AIML005", "department": "AI&ML", "designation": "Associate Professor"},
    
    # AI&DS Department
    {"name": "Dr. Neha Bansal", "register_no": "AIDS001", "department": "AI&DS", "designation": "Assistant Professor"},
    {"name": "Dr. Karthik Reddy", "register_no": "AIDS002", "department": "AI&DS", "designation": "Assistant Professor"},
    {"name": "Dr. Divya Krishnan", "register_no": "AIDS003", "department": "AI&DS", "designation": "Assistant Professor"},
    {"name": "Dr. Manish Kumar", "register_no": "AIDS004", "department": "AI&DS", "designation": "Associate Professor"},
    
    # ECE Department
    {"name": "Dr. Suresh Babu", "register_no": "ECE001", "department": "ECE", "designation": "Assistant Professor"},
    {"name": "Dr. Lakshmi Devi", "register_no": "ECE002", "department": "ECE", "designation": "Assistant Professor"},
    {"name": "Dr. Ravi Shankar", "register_no": "ECE003", "department": "ECE", "designation": "Assistant Professor"},
    {"name": "Dr. Sowmya Rao", "register_no": "ECE004", "department": "ECE", "designation": "Assistant Professor"},
    {"name": "Dr. Gopal Krishna", "register_no": "ECE005", "department": "ECE", "designation": "Associate Professor"},
    {"name": "Dr. Sudha Menon", "register_no": "ECE006", "department": "ECE", "designation": "Associate Professor"},
    
    # CYS Department (Cyber Security)
    {"name": "Dr. Harish Yadav", "register_no": "CYS001", "department": "CYS", "designation": "Assistant Professor"},
    {"name": "Dr. Swathi Pillai", "register_no": "CYS002", "department": "CYS", "designation": "Assistant Professor"},
    {"name": "Dr. Naveen Kumar", "register_no": "CYS003", "department": "CYS", "designation": "Assistant Professor"},
    {"name": "Dr. Archana Desai", "register_no": "CYS004", "department": "CYS", "designation": "Associate Professor"},
    
    # MECH Department
    {"name": "Dr. Prakash Nair", "register_no": "MECH001", "department": "MECH", "designation": "Assistant Professor"},
    {"name": "Dr. Geetha Ramesh", "register_no": "MECH002", "department": "MECH", "designation": "Assistant Professor"},
    {"name": "Dr. Vijay Kumar", "register_no": "MECH003", "department": "MECH", "designation": "Assistant Professor"},
    {"name": "Dr. Shweta Agarwal", "register_no": "MECH004", "department": "MECH", "designation": "Assistant Professor"},
    {"name": "Dr. Mohan Rao", "register_no": "MECH005", "department": "MECH", "designation": "Associate Professor"},
    
    # CSBS Department (Computer Science & Business Systems)
    {"name": "Dr. Arjun Malhotra", "register_no": "CSBS001", "department": "CSBS", "designation": "Assistant Professor"},
    {"name": "Dr. Nisha Bhatt", "register_no": "CSBS002", "department": "CSBS", "designation": "Assistant Professor"},
    {"name": "Dr. Sandeep Reddy", "register_no": "CSBS003", "department": "CSBS", "designation": "Assistant Professor"},
    {"name": "Dr. Pallavi Iyer", "register_no": "CSBS004", "department": "CSBS", "designation": "Associate Professor"},
    
    # S&H Department (Science & Humanities)
    {"name": "Dr. Madhavi Sharma", "register_no": "SNH001", "department": "S&H", "designation": "Assistant Professor"},
    {"name": "Dr. Ramesh Chand", "register_no": "SNH002", "department": "S&H", "designation": "Assistant Professor"},
    {"name": "Dr. Sunita Rao", "register_no": "SNH003", "department": "S&H", "designation": "Assistant Professor"},
    {"name": "Dr. Venkatesh Murthy", "register_no": "SNH004", "department": "S&H", "designation": "Assistant Professor"},
    {"name": "Dr. Rekha Menon", "register_no": "SNH005", "department": "S&H", "designation": "Associate Professor"},
    {"name": "Dr. Subramaniam Iyer", "register_no": "SNH006", "department": "S&H", "designation": "Associate Professor"},
]

print("Adding faculty members to database...")
print("=" * 60)

created_count = 0
existing_count = 0

for faculty_info in faculty_data:
    try:
        # Check if faculty already exists
        faculty, created = Faculty.objects.get_or_create(
            register_no=faculty_info['register_no'],
            defaults={
                'name': faculty_info['name'],
                'department': faculty_info['department']
            }
        )
        
        if created:
            # Set default password (same as register number for demo)
            faculty.set_password(faculty_info['register_no'])
            faculty.save()
            print(f"✓ Created: {faculty_info['name']} ({faculty_info['register_no']}) - {faculty_info['department']}")
            created_count += 1
        else:
            print(f"  Already exists: {faculty_info['name']} ({faculty_info['register_no']})")
            existing_count += 1
            
    except Exception as e:
        print(f"✗ Error adding {faculty_info['register_no']}: {str(e)}")

print("\n" + "=" * 60)
print(f"Summary:")
print(f"  Created: {created_count} faculty members")
print(f"  Already existed: {existing_count} faculty members")
print(f"  Total in database: {Faculty.objects.count()} faculty members")
print("\n" + "=" * 60)
print("\nFaculty by Department:")
from django.db.models import Count
for dept in Faculty.objects.values('department').annotate(count=Count('id')).order_by('department'):
    print(f"  {dept['department']}: {dept['count']} faculty members")
print("\nDefault password for all new faculty: <register_no>")
