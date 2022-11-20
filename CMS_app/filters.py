import django_filters
from django_filters import DateFilter
from django import forms
from CMS_app.models import Course, Employee


class CourseFilter(django_filters.FilterSet):

    # valori 'exact', 'istartswith', 'iendswith', 'icontains'
    course_name = django_filters.CharFilter(lookup_expr='icontains', label='Course name',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_date_gte = DateFilter(field_name='start_date', label='From date', lookup_expr='gte',
                                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    start_date_lte = DateFilter(field_name='start_date', label='To date', lookup_expr='lte',
                                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    # gte (greater than or egual to), lte (less than or equal to), gt (greater than), lt (less than)


    class Meta:
        model = Course
        fields = ['course_name', 'location', 'active']

    def __init__(self, *args, **kwargs):
        super(CourseFilter, self).__init__(*args, **kwargs)

        self.filters['course_name'].field.widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Course name'})
        self.filters['active'].field.widget.attrs.update(
            {'class': 'form-control'})


class EmployeeFilter(django_filters.FilterSet):

    first_name = django_filters.CharFilter(lookup_expr='istartswith', label='First name',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = django_filters.CharFilter(lookup_expr='icontains', label='Last name',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    # structure = django_filters.CharFilter(lookup_expr='icontains', label='Structure',
    #                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    # division = django_filters.CharFilter(lookup_expr='icontains', label='Structure',
    #                                       widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'active']

    def __init__(self, *args, **kwargs):
        super(EmployeeFilter, self).__init__(*args, **kwargs)

        self.filters['first_name'].field.widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'First name'})
        self.filters['last_name'].field.widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Last name'})
        # self.filters['structure_set'].field.widget.attrs.update(
        #     {'class': 'form-control'})
        # self.filters['division_set'].field.widget.attrs.update(
        #     {'class': 'form-control'})
        self.filters['active'].field.widget.attrs.update(
            {'class': 'form-control'})
