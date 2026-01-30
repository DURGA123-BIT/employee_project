from django.urls import path
from .views import report_dashboard, export_tasks_csv, export_tasks_excel, export_tasks_pdf

urlpatterns = [
    path('', report_dashboard, name="report_dashboard"),
    path('export/csv/', export_tasks_csv, name="export_tasks_csv"),
    path('export/excel/', export_tasks_excel, name="export_tasks_excel"),
    path('export/pdf/', export_tasks_pdf, name="export_tasks_pdf"),
]
