from accounts.models import User
from projects.models import Project
from activity_logs.models import ActivityLog
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, TaskComment
from .forms import TaskForm, EmployeeUpdateForm
from notifications.models import Notification
from datetime import date


# ===================== LIST VIEW =========================

@login_required
def task_list(request):
    user = request.user

    tasks = Task.objects.all()

    # Role filter
    if user.role == "MANAGER":
        tasks = tasks.filter(project__manager=user)
    elif user.role == "EMPLOYEE":
        tasks = tasks.filter(assigned_to=user)

    # FILTERS
    status = request.GET.get("status")
    priority = request.GET.get("priority")
    employee = request.GET.get("employee")
    project = request.GET.get("project")
    search = request.GET.get("search")

    if status and status != "ALL":
        tasks = tasks.filter(status=status)

    if priority and priority != "ALL":
        tasks = tasks.filter(priority=priority)

    if employee and employee != "ALL":
        tasks = tasks.filter(assigned_to__id=employee)

    if project and project != "ALL":
        tasks = tasks.filter(project__id=project)

    if search:
        tasks = tasks.filter(title__icontains=search)

    employees = User.objects.filter(role="EMPLOYEE")
    projects = Project.objects.all()

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "employees": employees,
        "projects": projects,
        "today": date.today(),
    })



# =================== CREATE TASK =========================

@login_required
def task_create(request):
    if request.user.role not in ["ADMIN", "MANAGER"]:
        return redirect('task-list')

    form = TaskForm(request.POST or None)

    if form.is_valid():
        task = form.save(commit=False)
        task.created_by = request.user
        task.save()

        # Activity log
        ActivityLog.objects.create(
            user=request.user,
            action=f"Created task: {task.title}"
        )

        # Notification
        Notification.objects.create(
            user=task.assigned_to,
            message=f"New task assigned: {task.title}"
        )

        return redirect('task-list')

    return render(request, "tasks/task_form.html", {"form": form})


# =================== UPDATE TASK =========================

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user.role == "EMPLOYEE":
        return redirect('task-employee-update', pk=pk)

    if request.user.role not in ["ADMIN", "MANAGER"]:
        return redirect('task-list')

    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()

        # Activity Log
        ActivityLog.objects.create(
            user=request.user,
            action=f"Updated task: {task.title}"
        )

        # Manager updates notify employee
        if request.user.role == "MANAGER":
            Notification.objects.create(
                user=task.assigned_to,
                message=f"Task updated by manager: {task.title}"
            )

        return redirect('task-list')

    return render(request, "tasks/task_form.html", {"form": form})


# =================== DELETE TASK =========================

@login_required
def task_delete(request, pk):
    if request.user.role not in ["ADMIN", "MANAGER"]:
        return redirect('task-list')

    task = get_object_or_404(Task, pk=pk)

    ActivityLog.objects.create(
        user=request.user,
        action=f"Deleted task: {task.title}"
    )

    task.delete()
    return redirect('task-list')


# =================== EMPLOYEE TASKS ======================

@login_required
def task_employee(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, "tasks/task_employee.html", {"tasks": tasks})


# ================= EMPLOYEE UPDATE =======================

@login_required
def task_employee_update(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    form = EmployeeUpdateForm(request.POST or None, instance=task)

    if request.method == "POST":
        if form.is_valid():
            form.save()

            # Log
            ActivityLog.objects.create(
                user=request.user,
                action=f"Employee updated task: {task.title} ({task.status})"
            )

            # Notify manager
            Notification.objects.create(
                user=task.project.manager,
                message=f"{request.user.username} updated task: {task.title}"
            )

            return redirect("task-employee")

    return render(request, "tasks/task_employee_update.html", {"form": form, "task": task})


# ================= MANAGER UPDATE =========================

@login_required
def task_employee_update(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)

    form = EmployeeUpdateForm(request.POST or None, instance=task)

    if request.method == "POST":
        if form.is_valid():
            form.save()

            # Optional: add comment
            comment = request.POST.get("comment")
            if comment:
                TaskComment.objects.create(
                    task=task,
                    user=request.user,
                    comment=comment
                )

            # Activity Log
            ActivityLog.objects.create(
                user=request.user,
                action=f"Employee updated task: {task.title} ({task.status})"
            )

            # Notify Manager
            Notification.objects.create(
                user=task.project.manager,
                message=f"{request.user.username} updated task: {task.title}"
            )

            return redirect("task-employee")

    return render(request, "tasks/task_employee_update.html", {
        "form": form,
        "task": task
    })



# ================= TASK DETAIL ============================

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = TaskComment.objects.filter(task=task)

    if request.method == "POST":
        TaskComment.objects.create(
            task=task,
            user=request.user,
            comment=request.POST.get("comment"),
            file=request.FILES.get("file")
        )
        return redirect('task-detail', pk=pk)

    return render(request, "tasks/task_detail.html", {
        "task": task,
        "comments": comments
    })



