from django import forms
from .models import Project
from accounts.models import User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'manager', 'employees', 'status']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'employees': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only MANAGER or ADMIN can manage employees
        self.fields['employees'].queryset = User.objects.filter(role="EMPLOYEE")

        # Only ADMIN can choose manager
        self.fields['manager'].queryset = User.objects.filter(role="MANAGER")
