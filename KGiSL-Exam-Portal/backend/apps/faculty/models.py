from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Faculty(models.Model):
    """
    Faculty model for storing faculty member details.
    Passwords are hashed using Django's password hashing utilities.
    """
    name = models.CharField(max_length=100)
    register_no = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=50)
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
