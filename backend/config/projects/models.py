from django.db import models
from users.models import User

class Project(models.Model):
    STATUS_CHOICES = (
        ('PLANNED', 'Planned'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()  
    end_date = models.DateField()   
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
