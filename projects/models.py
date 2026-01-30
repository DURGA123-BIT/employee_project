from django.conf import settings
from django.db import models

class Project(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="managed_projects")
    
    employees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_projects", blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
