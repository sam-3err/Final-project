from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny  # ✅ ADD THIS
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, UserDetailSerializer

# ✅ FIXED: Registration - No authentication required
@api_view(['POST'])
@permission_classes([AllowAny])  # ✅ THIS FIXES 401 ERROR
def register(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "User registered successfully!",
            "id": serializer.data['id']
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ FIXED: Login - No authentication required  
@api_view(['POST'])
@permission_classes([AllowAny])  # ✅ THIS TOO
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    
    user = User.objects.filter(email=email).first()
    
    if user and check_password(password, user.password):
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        })
    
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# ✅ Other views (profile, get_users) keep authentication
@api_view(['GET'])
def profile(request):
    return Response({"message": "Profile API working"})

@api_view(['GET'])
def get_users(request):
    users = User.objects.all().order_by('-created_at')
    serializer = UserDetailSerializer(users, many=True)
    return Response({
        "count": users.count(),
        "users": serializer.data,
        "stats": {
            "admins": User.objects.filter(role='ADMIN').count(),
            "managers": User.objects.filter(role='MANAGER').count(),
            "users": User.objects.filter(role='USER').count()
        }
    })
@api_view(['DELETE'])
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    
    # Don't delete yourself!
    if user.id == request.user.id:
        return Response({"error": "Cannot delete yourself!"}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    user.delete()
    return Response({"message": "User deleted successfully"}, 
                   status=status.HTTP_200_OK)