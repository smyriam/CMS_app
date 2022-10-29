from django import forms
from django.forms import TextInput, EmailInput, Select, DateInput, NumberInput
from CMS_app.models import Employee, Course, Division


class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    structure_options = (('central', 'Central'), ('regional', 'Regional'))
    structure = forms.ChoiceField(choices=structure_options)
    divisions = Division.objects.all()
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'structure', 'division', 'active']

        widgets = {
            'first_name' : TextInput(attrs={'autofocus': True, 'placeholder': 'Please enter first name', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'autofocus': True, 'placeholder': 'Please enter first name', 'class': 'form-control'}),
            'email' : EmailInput(attrs={'placeholder': 'Please enter email', 'class': 'form-control'}),
            'structure': Select(attrs={'class': 'form-select'}),
            'division' : Select(attrs={'class': 'form-select'})
        }


class AddCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

        widgets = {
            'course_name' : TextInput(attrs={'autofocus': True, 'placeholder': 'Please enter first name', 'class': 'form-control'}),
            'start_date' : DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date' : DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': Select(attrs={'class': 'form-select'}),
            'location_details' : TextInput(attrs={'class': 'form-control'}),
            'provider': TextInput(attrs={'class': 'form-control'}),
            'participation_fee' : NumberInput()
        }

