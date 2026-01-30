from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import UserForm
from projects.models import Project
from tasks.models import Task
from notifications.models import Notification


# ---------------- LOGIN ----------------

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard-redirect')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard-redirect')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


# --------------- DASHBOARD REDIRECT ----------------

@login_required
def dashboard_redirect(request):
    role = request.user.role

    if role == "ADMIN":
        return redirect('admin-dashboard')
    if role == "MANAGER":
        return redirect('manager-dashboard')
    if role == "EMPLOYEE":
        return redirect('employee-dashboard')

    return redirect('login')


# ---------------- ADMIN DASHBOARD ----------------

@login_required
def admin_dashboard(request):
    if request.user.role != "ADMIN":
        return redirect('dashboard-redirect')

    notifications = Notification.objects.filter(user=request.user, is_read=False)

    context = {
        "notifications": notifications,
        "notification_count": notifications.count(),
        "total_users": User.objects.count(),
        "total_projects": Project.objects.count(),
        "total_tasks": Task.objects.count(),
        "total_employees": User.objects.filter(role="EMPLOYEE").count(),
    }
    return render(request, "accounts/dashboard_admin.html", context)


# ---------------- MANAGER DASHBOARD ----------------

@login_required
def manager_dashboard(request):
    if request.user.role != "MANAGER":
        return redirect('dashboard-redirect')

    notifications = Notification.objects.filter(
        user=request.user, is_read=False
    ).order_by('-created_at')

    return render(request, "accounts/dashboard_manager.html", {
        "notifications": notifications,
        "notification_count": notifications.count(),
    })


# ---------------- EMPLOYEE DASHBOARD ----------------

@login_required
def employee_dashboard(request):
    if request.user.role != "EMPLOYEE":
        return redirect('dashboard-redirect')

    notifications = Notification.objects.filter(
        user=request.user, is_read=False
    ).order_by('-created_at')

    # Mark as read after opening dashboard
    notifications.update(is_read=True)

    return render(request, "accounts/dashboard_employee.html", {
        "notifications": notifications,
        "notification_count": notifications.count(),
    })


# ---------------- LOGOUT ----------------

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- ADMIN USER MANAGEMENT ----------------

@login_required
def user_list(request):
    if request.user.role != "ADMIN":
        return redirect('dashboard-redirect')

    users = User.objects.all()
    return render(request, "accounts/user_list.html", {"users": users})


@login_required
def user_create(request):
    if request.user.role != "ADMIN":
        return redirect('dashboard-redirect')

    form = UserForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)

        from django.contrib.auth.hashers import make_password
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        return redirect('user-list')

    return render(request, "accounts/user_form.html", {"form": form})
