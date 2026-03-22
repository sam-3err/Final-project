from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    ROLE_CHOICES = (
        ('ADMIN','Admin'),
        ('MANAGER','Manager'),
        ('USER','User'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Fixed typo: updated_At → updated_at

    def __str__(self):
        return f"{self.name} ({self.role})"

    # ✅ NEW: Override save() to hash passwords automatically
    def save(self, *args, **kwargs):
        # Hash password if it's raw (not already hashed)
        if self.password and not self.password.startswith(('pbkdf2', 'bcrypt', 'argon2', '$2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
