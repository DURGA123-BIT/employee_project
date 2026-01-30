from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm


@login_required
def project_list(request):
    if request.user.role == "EMPLOYEE":
        projects = Project.objects.filter(employees=request.user)
    else:
        projects = Project.objects.all()

    return render(request, "projects/project_list.html", {"projects": projects})


@login_required
def project_create(request):
    if request.user.role not in ["ADMIN", "MANAGER"]:
        return redirect('dashboard-redirect')

    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save()
        return redirect('project-list')

    return render(request, "projects/project_form.html", {"form": form})


@login_required
def project_update(request, pk):
    if request.user.role not in ["ADMIN", "MANAGER"]:
        return redirect('dashboard-redirect')

    project = get_object_or_404(Project, id=pk)
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect('project-list')

    return render(request, "projects/project_form.html", {"form": form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, id=pk)
    return render(request, "projects/project_detail.html", {"project": project})


@login_required
def project_delete(request, pk):
    if request.user.role not in ["ADMIN", "MANAGER"]:
        return redirect('dashboard-redirect')

    project = get_object_or_404(Project, id=pk)
    project.delete()
    return redirect('project-list')
