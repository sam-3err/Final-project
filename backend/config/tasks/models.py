from django.db import models
from users.models import User
from projects.models import Project

class Task(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    priority = models.CharField(max_length=20, default='MEDIUM')
    due_date = models.DateField()
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    
    def __str__(self):
        return f"{self.title} - {self.assigned_user.name}"
# ADD THIS AT BOTTOM of your existing tasks/models.py
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}: {self.text[:50]}"

    class Meta:
        ordering = ['-created_at']
