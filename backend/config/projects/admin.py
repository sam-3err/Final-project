from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'start_date', 'end_date', 'created_by']
    list_filter = ['status', 'created_by']
    search_fields = ['name']
