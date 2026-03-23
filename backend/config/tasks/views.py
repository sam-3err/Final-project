from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from rest_framework import status
from .models import Task,Comment
from .serializers import TaskSerializer,CommentSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response({
        "data": serializer.data,
        "count": len(serializer.data)
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def create_task(request):
    print(" TASK RAW DATA:", request.data)
    print(" ASSIGNED_USER:", request.data.get('assigned_user'))
    print(" PROJECT:", request.data.get('project'))

    try:
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            print("✅ TASK SAVED ID:", task.id)
            return Response({"message": "Task assigned successfully!"})

        print("❌ TASK ERRORS:", serializer.errors)
        return Response({
            "error": "Task validation failed",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("🚨 UNEXPECTED ERROR:", str(e))
        return Response({
            "error": "Server error",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def update_task(request, id):  
    print(" UPDATING TASK:", id)
    print(" DATA:", request.data)

    try:
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            print("✅ TASK UPDATED:", task.id, task.status)
            return Response({"message": "Task updated successfully!"})

        print("❌ SERIALIZER ERRORS:", serializer.errors)
        return Response(
            {"error": "Validation failed", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    except Task.DoesNotExist:
        print("❌ Task not found:", id)
        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        print("🚨 UNEXPECTED ERROR:", str(e))
        return Response(
            {"error": "Server error", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@api_view(['POST'])
def add_task_comment(request, task_id):
    print(f"🔥 DEBUG START - task_id={task_id}")
    print(f"🔥 DATA: {request.data}")
    print(f"🔥 USER: {request.user}")
    
    try:
        # Test 1: Check Task exists
        task = Task.objects.get(id=task_id)
        print(f"✅ Task found: {task.title}")
        
        # Test 2: Check/Create user
        if request.user.is_authenticated:
            user = request.user
        else:
            from users.models import User
            user = User.objects.first()  # First user as fallback
        print(f"✅ User: {user}")
        
        # Test 3: Create comment
        comment = Comment.objects.create(
            task=task,
            user=user,
            text=request.data.get('text', 'DEBUG comment')
        )
        print(f"✅ Comment created ID: {comment.id}")
        
        from .serializers import CommentSerializer
        serializer = CommentSerializer(comment)
        print(f"✅ Serializer OK")
        
        return Response(serializer.data, status=201)
        
    except Task.DoesNotExist:
        print("❌ Task not found!")
        return Response({'error': 'Task not found'}, status=404)
    except Exception as e:
        print(f"💥 FULL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return Response({'error': f'{e}'}, status=500)

def get_tasks(request):
    tasks = Task.objects.select_related('assigned_to', 'project').prefetch_related('comments_set')[:]
    serializer = TaskSerializer(tasks, many=True, context={'request': request})
    return Response(serializer.data)
@api_view(['GET'])
def user_tasks(request):
    user_id = request.query_params.get('assigned_to')
    tasks = Task.objects.filter(assigned_to_id=user_id).prefetch_related('comments__user')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
