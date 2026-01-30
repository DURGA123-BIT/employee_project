from django.urls import path
from .views import (
    task_list,
    task_create,
    task_update,
    task_delete,
    task_employee,
    task_employee_update,
    task_detail,
)

urlpatterns = [
    path('', task_list, name='task-list'),
    path('create/', task_create, name='task-create'),

    # employee related
    path('employee/', task_employee, name='task-employee'),
    path('employee/<int:pk>/update/', task_employee_update, name='task-employee-update'),

    # main task actions
    path('<int:pk>/', task_detail, name='task-detail'),
    path('edit/<int:pk>/', task_update, name='task-update'),
    path('delete/<int:pk>/', task_delete, name='task-delete'),
]
