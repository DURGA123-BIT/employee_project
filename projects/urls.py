from django.urls import path
from .views import (
    project_list,
    project_create,
    project_update,
    project_detail,
    project_delete,
)

urlpatterns = [
    path('', project_list, name='project-list'),
    path('create/', project_create, name='project-create'),
    path('<int:pk>/', project_detail, name='project-detail'),
    path('<int:pk>/edit/', project_update, name='project-update'),
    path('<int:pk>/delete/', project_delete, name='project-delete'),
]
