import django_filters
from django_filters import DateFilter
from django import forms
from CMS_app.models import Course


class CourseFilter(django_filters.FilterSet):

    course_name = django_filters.CharFilter(lookup_expr='icontains', label='Course name',
                                           widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    # valori 'exact', 'istartswith', 'iendswith', 'icontains'
    # gte (greater than or egual to), lte (less than or equal to), gt (greater than), lt (less than)
    start_date_gte = DateFilter(field_name='start_date', label='From date', lookup_expr='gte',
                                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    start_date_lte = DateFilter(field_name='start_date', label='To date', lookup_expr='lte',
                                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Course
        fields = ['course_name', 'start_date', 'active']

    def __init__(self, *args, **kwargs):
        super(CourseFilter, self).__init__(*args, **kwargs)

        self.filters['course_name'].field.widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Course name'})
        self.filters['active'].field.widget.attrs.update(
            {'class': 'form-control'})
