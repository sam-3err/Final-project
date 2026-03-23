from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'priority', 'assigned_user', 'project']
    list_filter = ['status', 'priority', 'assigned_user']
    search_fields = ['title']
