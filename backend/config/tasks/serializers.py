from rest_framework import serializers
from .models import Task, Project, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.name', read_only=True)
    created_at = serializers.DateTimeField(format='%b %d %H:%M', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
