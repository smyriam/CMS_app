from django import forms
from django.forms import TextInput, EmailInput, Select

from CMS_app.models import Employee


class AddEmployee(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

        widgets = {
            'first_name' : TextInput(attrs={'autofocus': True, 'placeholder': 'Please enter first name', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'autofocus': True, 'placeholder': 'Please enter first name', 'class': 'form-control'}),
            'email' : EmailInput(attrs={'placeholder': 'Please enter email', 'class': 'form-control'}),
            'structure' : Select(attrs={'class': 'form-select'})
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'structure', 'division', 'active']