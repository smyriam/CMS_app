from django import forms
from django.forms import TextInput, EmailInput, Select, DateInput, NumberInput
from CMS_app.models import Employee, Course, Division


class AddEmployeeForm(forms.ModelForm):
    # divisions = Division.objects.all()
    # division_list = []
    # try:
    #     divisions = Division.objects.all()
    #     for division in divisions:
    #         small_list = (division.id, division.division_name)
    #         division_list.append(small_list)
    # except:
    #     division_list = []
    #
    # division = forms.ChoiceField(label="Division", choices="division_list",
    #                              widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    structure_options = (('Central', 'Central'), ('Regional', 'Regional'))
    structure = forms.ChoiceField(choices=structure_options)
    division_list = []
    try:
        divisions = Division.objects.all()
        for division in divisions:
            small_list = (division.id, division.division_name)
            division_list.append(small_list)
    except:
        division_list = []

    division = forms.ChoiceField(label="Division", choices="division_list", widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'structure', 'active']


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
