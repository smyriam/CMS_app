from django import forms
from django.forms import TextInput, EmailInput, Select, DateInput, NumberInput
from CMS_app.models import Employee, Course, Division, CourseEmployee


class AddEmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'email', 'structure', 'active']


class EmployeeForm(forms.ModelForm):
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
        fields = ['first_name', 'last_name', 'email', 'structure', 'division', 'active']


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
                    'active': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['division'].queryset = Division.objects.none()

        if 'division' in self.data:
            try:
                structure_id = int(self.data.get('structure'))
                self.fields['division'].queryset = Division.objects.filter(structure_id=structure_id).order_by('division')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['division'].queryset = self.instance.structure.division_set.order_by('division')


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class AssignCourseForm(forms.ModelForm):
    class Meta:
        model = CourseEmployee
        fields = ['source_of_funding', 'duration', 'transport_costs', 'accommodation_costs', 'allowance_costs']

        widgets = {
            'source_of_funding': Select(attrs={'class': 'form-select'}),
            'duration': NumberInput(attrs={'placeholder': 'Enter course duration',
                'class': 'form-control'}),
            'transport_costs': NumberInput(attrs={'placeholder': 'Enter transport cost',
                'class': 'form-control'}),
            'accommodation_costs': NumberInput(attrs={'placeholder': 'Enter accomodation cost',
                'class': 'form-control'}),
            'allowance_costs': NumberInput(attrs={'placeholder': 'Enter allowance cost',
                'class': 'form-control'}),
        }

    # def clean(self):
    #     cleaned_data = self.cleaned_data  # veti avea un dictionar cu toate valorile introduse in dictionar
    #     all_students = Student.objects.all()  # interogati bd unde veti stoca toti studentii salvati in db
    #     for student in all_students:  # iterez fiecare student salvat in db
    #         if student.first_name == cleaned_data['first_name'] and student.last_name == cleaned_data['last_name']:
    #             msg = f'This first name {cleaned_data["first_name"]} and ' \
    #                   f'this last name {cleaned_data["last_name"]} exists in db'
    #             self._errors['first_name'] = self.error_class([msg])

        # return cleaned_data