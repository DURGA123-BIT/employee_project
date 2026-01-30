from django import forms
from .models import Task
from accounts.models import User

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'due_date', 'priority', 'status', 'progress']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'progress': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only Employees should show for assignment
        self.fields['assigned_to'].queryset = User.objects.filter(role="EMPLOYEE")

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'progress']

        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
        }
