from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import  IsAuthenticated  ,AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer
from django.shortcuts import get_object_or_404
from .serializers import ProjectSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Your custom permission (create this if missing)

@api_view(['GET'])
@permission_classes([AllowAny])
def project_dashboard(request):
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status="ACTIVE").count()
    return Response({
        "total_projects": total_projects,
        "active_projects": active_projects,
        "completed_projects": Project.objects.filter(status="COMPLETED").count(),
        "planned_projects": Project.objects.filter(status="PLANNED").count()
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def create_project(request):
    print("✅ Project data:", request.data)
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        project = serializer.save()
        print("✅ Project SAVED:", project.id)
        return Response({
            "message": "Project created successfully!",
            "project": ProjectSerializer(project).data
        }, status=status.HTTP_201_CREATED)
    print("Errors:", serializer.errors)
    return Response({
        "error": "Validation failed",
        "details": serializer.errors
    }, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response({
        "message": "Projects fetched successfully",
        "data": serializer.data,
        "count": len(serializer.data)
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_project(request, id):
    try:
        project = Project.objects.get(id=id)
        serializer = ProjectSerializer(project)
        return Response({
            "message": "Project fetched successfully",
            "data": serializer.data
        })
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_project(request, id):
    try:
        project = Project.objects.get(id=id)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Project updated successfully",
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_project(request, id):
    try:
        project = Project.objects.get(id=id)
        project.delete()
        return Response({"message": "Project deleted successfully"})
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
@api_view(['PATCH'])  # Only PATCH method
@permission_classes([AllowAny])  # ← BYPASS ALL PERMISSIONS (TEMP FIX)
def update_project(request, id):
    project = get_object_or_404(Project, id=id)
    serializer = ProjectSerializer(project, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)