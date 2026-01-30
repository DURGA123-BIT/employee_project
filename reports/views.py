import csv
from django.http import HttpResponse
from django.shortcuts import render
from tasks.models import Task
from projects.models import Project
from accounts.models import User
from openpyxl import Workbook
from reportlab.pdfgen import canvas


def report_dashboard(request):

    tasks = Task.objects.all()

    # ---- FILTERS ----
    status = request.GET.get("status")
    priority = request.GET.get("priority")
    from_date = request.GET.get("from")
    to_date = request.GET.get("to")

    if status and status != "ALL":
        tasks = tasks.filter(status=status)

    if priority and priority != "ALL":
        tasks = tasks.filter(priority=priority)

    if from_date:
        tasks = tasks.filter(due_date__gte=from_date)

    if to_date:
        tasks = tasks.filter(due_date__lte=to_date)

    # ---- DASHBOARD METRICS ----
    total_projects = Project.objects.count()
    total_tasks = tasks.count()

    completed_tasks = tasks.filter(status="COMPLETED").count()
    ongoing_tasks = tasks.filter(status="ONGOING").count()
    pending_tasks = tasks.filter(status="PENDING").count()

    total_employees = User.objects.filter(role="EMPLOYEE").count()

    # ---- FOR CHARTS ----
    pie_labels = ["Completed", "Ongoing", "Pending"]
    pie_data = [completed_tasks, ongoing_tasks, pending_tasks]

    bar_labels = ["Completed", "Ongoing", "Pending"]
    bar_data = [completed_tasks, ongoing_tasks, pending_tasks]

    context = {
        "tasks": tasks,
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "ongoing_tasks": ongoing_tasks,
        "pending_tasks": pending_tasks,
        "total_employees": total_employees,
        "pie_labels": pie_labels,
        "pie_data": pie_data,
        "bar_labels": bar_labels,
        "bar_data": bar_data,
        "filters": {
            "status": status or "ALL",
            "priority": priority or "ALL",
            "from_date": from_date or "",
            "to_date": to_date or "",
        }
    }

    return render(request, "reports/dashboard.html", context)


# ------------------- EXPORT CSV -----------------------------------

def export_tasks_csv(request):
    tasks = Task.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tasks.csv'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Status', 'Priority', 'Due Date', 'Assigned To'])

    for t in tasks:
        writer.writerow([t.title, t.status, t.priority, t.due_date, t.assigned_to])

    return response


# ------------------- EXPORT EXCEL -----------------------------------

def export_tasks_excel(request):
    tasks = Task.objects.all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Tasks"

    ws.append(['Title', 'Status', 'Priority', 'Due Date', 'Assigned To'])

    for t in tasks:
        ws.append([t.title, t.status, t.priority, t.due_date, t.assigned_to.username])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename=tasks.xlsx'
    wb.save(response)
    return response


# ------------------- EXPORT PDF -----------------------------------

def export_tasks_pdf(request):
    tasks = Task.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=tasks.pdf'

    p = canvas.Canvas(response)
    y = 800

    p.drawString(240, y, "TASK REPORT")
    y -= 40

    for t in tasks:
        txt = f"{t.title} | {t.status} | {t.priority} | {t.due_date} | {t.assigned_to.username}"
        p.drawString(50, y, txt)
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response
