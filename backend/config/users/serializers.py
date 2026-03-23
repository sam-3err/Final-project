from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

# NEW SERIALIZER for Admin dashboard
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'created_at', 'updated_at']
