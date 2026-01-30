from django.urls import path
from .views import activity_log_list

urlpatterns = [
    path('', activity_log_list, name='activity-logs'),
]
