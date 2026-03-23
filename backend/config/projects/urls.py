from django.urls import path
from .views import *

urlpatterns = [

    path('create/', create_project),
    path('', get_projects),
    path('<int:id>/', get_project),
    path('update/<int:id>/', update_project),
    path('delete/<int:id>/', delete_project),
    path('dashboard/', project_dashboard),
]