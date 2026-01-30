from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ActivityLog

@login_required
def activity_log_list(request):
    if request.user.role not in ["ADMIN", "MANAGER"]:
        return redirect('dashboard-redirect')

    logs = ActivityLog.objects.all().order_by('-created_at')
    return render(request, "activity_logs/log_list.html", {"logs": logs})
