from django.urls import path
from .views import (
    login_view,
    logout_view,
    dashboard_redirect,
    admin_dashboard,
    manager_dashboard,
    employee_dashboard,
    user_list,
    user_create,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('dashboard/', dashboard_redirect, name='dashboard-redirect'),
    path('admin/', admin_dashboard, name='admin-dashboard'),
    path('manager/', manager_dashboard, name='manager-dashboard'),
    path('employee/', employee_dashboard, name='employee-dashboard'),

    path('users/', user_list, name='user-list'),
    path('users/create/', user_create, name='user-create'),
]
