from django.urls import path
from .views import task_list, create_task, update_task, user_tasks
from . import views
urlpatterns = [
    path('', task_list),  
    path('create/', create_task),
    path('update/<int:id>/', update_task),
    path('user/<int:user_id>/', user_tasks),
    path('<int:task_id>/comment/', views.add_task_comment),  # POST comment

]