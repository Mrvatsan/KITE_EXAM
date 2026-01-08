from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Faculty(models.Model):
    """
    Faculty model for storing faculty member details.
    Passwords are hashed using Django's password hashing utilities.
    """
    name = models.CharField(max_length=100)
    register_no = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Hashed password

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verify the password against the stored hash."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.register_no}) - {self.department}"

    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'
        ordering = ['department', 'name']


class FacultyAllocation(models.Model):
    """
    Tracks faculty-to-hall assignments for specific exam dates and sessions.
    Enforces uniqueness: one faculty can only have one assignment per date-session.
    """
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='allocations')
    hall_no = models.CharField(max_length=50)
    course_code = models.CharField(max_length=100)
    course_title = models.CharField(max_length=300)
    exam_date = models.DateField()
    session = models.CharField(max_length=20)
    is_replaced = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    replaced_by = models.ForeignKey(
        Faculty, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='replacements'
    )
    reason_for_unavailability = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Faculty Allocation'
        verbose_name_plural = 'Faculty Allocations'
        ordering = ['exam_date', 'session', 'hall_no']
        # Ensure one faculty cannot be assigned multiple halls in the same session
        unique_together = [['faculty', 'exam_date', 'session']]

    def __str__(self):
        return f"{self.faculty.name} - Hall {self.hall_no} - {self.exam_date} ({self.session})"


class FacultyRotationState(models.Model):
    """
    Persists the rotation state for each department and designation to ensure fair distribution
    of invigilation duties across faculty members.
    """
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, default='Professor')
    last_row_index = models.IntegerField(default=-1)
    academic_year = models.CharField(max_length=20, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Faculty Rotation State'
        verbose_name_plural = 'Faculty Rotation States'
        unique_together = [['department', 'designation']]

    def __str__(self):
        return f"{self.department} ({self.designation}) - Last Index: {self.last_row_index}"


class FacultyAllocationStatus(models.Model):
    """
    Tracks the confirmation and visibility status of faculty allocations 
    for a specific date and session.
    """
    exam_date = models.DateField()
    session = models.CharField(max_length=20)
    is_confirmed = models.BooleanField(default=False)
    is_faculty_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Faculty Allocation Status'
        verbose_name_plural = 'Faculty Allocation Statuses'
        unique_together = [['exam_date', 'session']]

    def __str__(self):
        return f"{self.exam_date} ({self.session}) - Confirmed: {self.is_confirmed}, Active: {self.is_faculty_active}"


import secrets
from django.utils import timezone

class FacultyToken(models.Model):
    """
    Custom token model for Faculty authentication to ensure complete isolation
    from Admin and Student authentication systems.
    """
    key = models.CharField(max_length=100, primary_key=True)
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE, related_name='auth_token')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_urlsafe(64)
        if not self.expires_at:
            # Token expires in 24 hours
            self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        return super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Token for {self.faculty.name}"
