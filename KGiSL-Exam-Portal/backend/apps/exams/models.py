from django.db import models

class Dataset(models.Model):
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Dataset {self.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

class Student(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='students')
    register_no = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=50)
    course_title = models.CharField(max_length=100)
    exam_date = models.DateField(null=True, blank=True)
    session = models.CharField(max_length=20)
    hall_no = models.CharField(max_length=50)
    seat_no = models.CharField(max_length=50)
    password = models.CharField(max_length=100, default='Kite@12345')

    class Meta:
        # Constraint to ensure unique register_no per dataset if needed, 
        # or globally if we assume one active exam at a time.
        # User said: "If the admin has Deactivated the dataset, show 'Pending for admin access'".
        # This implies multiple datasets can exist but only one is active. 
        # So uniqueness should be per dataset? Or just rely on the active dataset filter.
        # Let's keep it simple.
        pass

    def __str__(self):
        return f"{self.register_no} - {self.name}"

class HallTicketExam(models.Model):
    """
    Stores exam schedule data for hall tickets.
    Data is organized by department and semester.
    """
    department = models.CharField(max_length=50)  # AI&ML, AI&DS, CSE, ECE, IT, MECH, R&A, CSBS, CYS
    semester = models.CharField(max_length=10)    # I, II, III, IV, V, VI, VII, VIII
    course_code = models.CharField(max_length=100)  # Increased to handle longer codes
    course_title = models.CharField(max_length=300)  # Increased to handle longer titles
    exam_date = models.DateField()
    session = models.CharField(max_length=10)     # FN or AN
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['exam_date', 'session']
        verbose_name = 'Hall Ticket Exam'
        verbose_name_plural = 'Hall Ticket Exams'
    
    def __str__(self):
        return f"{self.department} - Sem {self.semester} - {self.course_code}"
