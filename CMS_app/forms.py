from django import forms
from django.forms import Select, NumberInput
from CMS_app.models import Employee, Course, Division, CourseEmployee, Funding


class AddEmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'email', 'structure', 'active']


class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
                    'first_name': forms.TextInput(attrs={'class':'form-control'}),
                    'last_name': forms.TextInput(attrs={'class':'form-control'}),
                    'email': forms.EmailInput(attrs={'class':'form-control'}),
                    'structure': forms.Select(attrs={'class':'form-control'}),
                    'division': forms.Select(attrs={'class': 'form-control'}),
                    'active': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['division'].queryset = Division.objects.none()

        if 'division' in self.data:
            try:
                structure_id = int(self.data.get('structure'))
                self.fields['division'].queryset = Division.objects.filter(structure_id=structure_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['division'].queryset = self.instance.structure.division_set.order_by('name')


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class EditCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
                    'course_name': forms.TextInput(attrs={'class':'form-control'}),
                    'start_date': forms.DateInput(attrs={'class':'form-control'}),
                    'duration': forms.NumberInput(attrs={'class': 'form-control'}),
                    'provider': forms.TextInput(attrs={'class': 'form-control'}),
                    'location': forms.Select(attrs={'class': 'form-control'}),
                    'location_details': forms.TextInput(attrs={'class':'form-control'}),
                    'participation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
                    'active': forms.CheckboxInput(),
        }


class AssignCourseForm(forms.ModelForm):
    class Meta:
        model = CourseEmployee
        fields = ['course', 'structure', 'division', 'transport_costs', 'accommodation_costs', 'allowance_costs']

        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'structure': forms.Select(attrs={'class':'form-control'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
            'transport_costs': forms.NumberInput(attrs={'class': 'form-control'}),
            'accommodation_costs': forms.NumberInput(attrs={'class': 'form-control'}),
            'allowance_costs': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['division'].queryset = Funding.objects.none()

        if 'division' in self.data:
            try:
                structure_id = int(self.data.get('structure'))
                self.fields['division'].queryset = Funding.objects.filter(structure_id=structure_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['division'].queryset = self.instance.structure.division_set.order_by('name')


class AssignEmployeeForm(forms.ModelForm):
    class Meta:
        model = CourseEmployee
        fields = ['employee', 'structure', 'division', 'transport_costs', 'accommodation_costs', 'allowance_costs']

        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'structure': forms.Select(attrs={'class':'form-control'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
            'transport_costs': forms.NumberInput(attrs={'class': 'form-control'}),
            'accommodation_costs': forms.NumberInput(attrs={'class': 'form-control'}),
            'allowance_costs': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['division'].queryset = Funding.objects.none()

        if 'division' in self.data:
            try:
                structure_id = int(self.data.get('structure'))
                self.fields['division'].queryset = Funding.objects.filter(structure_id=structure_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['division'].queryset = self.instance.structure.division_set.order_by('name')


class EditAssignForm(forms.ModelForm):
    class Meta:
        model = CourseEmployee
        fields = ['structure', 'division', 'transport_costs', 'accommodation_costs', 'allowance_costs']

        widgets = {
            'structure': forms.Select(attrs={'class':'form-control'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
            'transport_costs': forms.NumberInput(attrs={'class': 'form-control'}),
            'accommodation_costs': forms.NumberInput(attrs={'class': 'form-control'}),
            'allowance_costs': forms.NumberInput(attrs={'class': 'form-control'}),
        }

