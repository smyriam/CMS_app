from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView

from CMS_app.filters import CourseFilter, EmployeeFilter
from CMS_app.forms import AddEmployeeForm, AddCourseForm, EditEmployeeForm, EditCourseForm, AssignCourseForm, \
    AssignEmployeeForm, EditAssignForm
from CMS_app.backend import Backend
from CMS_app.models import Employee, Course, CourseEmployee, Division, Funding
from django.db.models import Sum


# Create your views here.
def show_base(request):
    return render(request, "base.html")


def show_login_page(request):
    return render(request, "login.html")


def do_login(request):
    if request.method != "POST":
        return HttpResponse("<h2>Not allowed</h2>")
    else:
        user = Backend.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            return HttpResponseRedirect('/home')
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


@login_required
def user_details(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email)
    else:
        return HttpResponse("Please, login first")


@login_required
def do_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def reset_password(request):
    return render(request, "reset_password.html")


@login_required
def admin_home(request):
    employees_count = Employee.objects.all().count()
    courses_count = Course.objects.all().count()
    transport = list(CourseEmployee.objects.aggregate(Sum('transport_costs')).values())[0]
    transport_costs = int(transport)
    accommodation = list(CourseEmployee.objects.aggregate(Sum('accommodation_costs')).values())[0]
    accommodation_costs = int(accommodation)
    allowance_costs = list(CourseEmployee.objects.aggregate(Sum('allowance_costs')).values())[0]
    total_days = list(CourseEmployee.objects.aggregate(Sum('duration')).values())[0]

    select = CourseEmployee.objects.all()
    fee = []
    for i in select:
        fee.append(Course.objects.filter(id=i.course_id).values_list('participation_fee', flat=True).first())
    participation_fee = sum(fee)

    return render(request, "dashboard/dashboard.html",
        {
            "employees_count": employees_count,
            "courses_count": courses_count,
            "transport_costs": transport_costs,
            "accommodation_costs": accommodation_costs,
            "allowance_costs": allowance_costs,
            "total_days": total_days,
            "participation_fee": participation_fee
        })


def employee_details(request, pk):
    # Employee data
    employee = Employee.objects.filter(id=pk).get()

    # Get employee courses
    selects = CourseEmployee.objects.filter(employee_id=pk).all()
    courses = []
    for i in selects:
        courses.append(Course.objects.filter(id=i.course_id).first())

    # Get transport costs
    transport = []
    for i in selects:
        transport.append(
            CourseEmployee.objects.filter(course_id=i.course_id, employee_id=pk).values_list('transport_costs',
                                                                                             flat=True).first())
    transport_costs = sum(transport)

    # Get accomodation costs
    accomodation = []
    for i in selects:
        accomodation.append(
            CourseEmployee.objects.filter(course_id=i.course_id, employee_id=pk).values_list('accommodation_costs',
                                                                                             flat=True).first())
    accommodation_costs = sum(accomodation)

    # Get allowance costs
    allowance = []
    for i in selects:
        allowance.append(
            CourseEmployee.objects.filter(course_id=i.course_id, employee_id=pk).values_list('allowance_costs',
                                                                                             flat=True).first())
    allowance_costs = sum(allowance)

    # Get participation fee costs
    course_fee = []
    for i in selects:
        course_fee.append(Course.objects.filter(id=i.course_id).values_list('participation_fee', flat=True).first())
    course_fee = sum(course_fee)

    context = {
        'courses': courses,
        'employee': employee,
        'transport_costs': transport_costs,
        'accomodation_costs': accommodation_costs,
        'allowance_costs': allowance_costs,
        'course_fee': course_fee,
    }

    return render(request, 'employee/employee_details.html', context)


@login_required
def add_employee(request):
    if request.method == "POST":
        form = AddEmployeeForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return JsonResponse({'msg': 'Data saved'})

        else:
            print("ERROR, FORM INVALID")
            return JsonResponse({'msg': 'ERROR, FORM INVALID'})
    else:
        form = AddEmployeeForm()
    return JsonResponse({'form': form})


@login_required
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EditEmployeeForm(instance=employee)
    if request.method == 'POST':
        form = EditEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee successfully updated')
            return redirect('list-of-employees')
    return render(request, 'employee/edit_employee_template.html', {'form': form})


@login_required
def load_divisions(request):
    structure_id = request.GET.get('structure_id')
    divisions = Division.objects.filter(structure_id=structure_id).all()
    return render(request, 'employee/division_options.html', {'divisions': divisions})


class EmployeesList(ListView):
    template_name = 'employee/list_of_employees.html'
    model = Employee
    context_object_name = 'all_employees'

    def get_context_data(self, **kwargs):
        data = super(EmployeesList, self).get_context_data(**kwargs)
        employees = Employee.objects.all()
        my_filter = EmployeeFilter(self.request.GET, queryset=employees)
        employees = my_filter.qs
        data['all_employees'] = employees
        data['my_filter'] = my_filter

        return data


@login_required
def delete_employee(request, pk):
    Employee.objects.filter(id=pk).delete()
    return redirect('list-of-employees')


@login_required
def add_course(request):
    if request.method == "POST":
        form = AddCourseForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Data Saved")
            return JsonResponse({'msg': 'Data saved'})

        else:
            print(form)
            print("ERROR, FORM INVALID")
            return JsonResponse({'msg': 'ERROR, FORM INVALID'})
    else:
        form = AddCourseForm()
    return JsonResponse({'form': form})


@login_required
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = EditCourseForm(instance=course)
    if request.method == 'POST':
        form = EditCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course successfully updated')
            return redirect('list-of-courses')
    return render(request, 'course/edit_course_template.html', {'form': form})


class CoursesList(LoginRequiredMixin, ListView):
    template_name = 'course/list_of_courses.html'
    model = Course
    context_object_name = 'all_courses'

    def get_context_data(self, **kwargs):
        data = super(CoursesList, self).get_context_data(**kwargs)
        courses = Course.objects.all()
        my_filter = CourseFilter(self.request.GET, queryset=courses)
        courses = my_filter.qs
        data['all_courses'] = courses
        data['my_filter'] = my_filter

        return data


@login_required
def delete_course(request, pk):
    Course.objects.filter(id=pk).delete()
    return redirect('list-of-courses')


class CourseDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'course/course_details.html'
    model = Course

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        selects = CourseEmployee.objects.filter(course_id=self.kwargs['pk']).all()
        employees = []
        for i in selects:
            employees.append(Employee.objects.filter(id=i.employee_id).first())
        data['employees'] = employees

        return data


@login_required
def assign_course(request, pk):
    employee_data = Employee.objects.get(id=pk)
    form = AssignCourseForm()
    if request.method == 'POST':
        form = AssignCourseForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee_id = employee_data.id
            instance.duration = Course.objects.get(id=request.POST.get('course')).duration
            instance.save()
            messages.success(request, 'Course successfully assigned')
            return redirect('view-employee', pk)
    return render(request, 'employee/assign_course_template.html',
                  {'form': form, 'first_name': employee_data.first_name, 'last_name': employee_data.last_name})


@login_required
def assign_employee(request, pk):
    course_data = Course.objects.get(id=pk)
    form = AssignEmployeeForm()
    if request.method == 'POST':
        form = AssignEmployeeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.course_id = course_data.id
            instance.duration = course_data.duration
            instance.save()
            messages.success(request, 'Employee successfully assigned')
            return redirect('view-course', pk)
    return render(request, 'course/assign_employee_template.html',
                  {'form': form, 'course_name': course_data.course_name})


@login_required
def edit_assign(request, pk, cid):
    assign = get_object_or_404(CourseEmployee, employee=pk, course=cid)
    form = EditAssignForm(instance=assign)
    if request.method == 'POST':
        form = EditAssignForm(request.POST, instance=assign)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.course_id = cid
            instance.employee_id = pk
            instance.save()
            messages.success(request, 'Assignment updated successfully')
            return redirect('view-course', cid)
    return render(request, 'course/edit_assign.html',
                  {'form': form, 'first_name': assign.employee.first_name, 'last_name': assign.employee.last_name,
                   'course_name': assign.course.course_name})


@login_required
def load_fundings(request):
    structure_id = request.GET.get('structure_id')
    divisions = Funding.objects.filter(structure_id=structure_id).all()
    return render(request, 'employee/division_options.html', {'divisions': divisions})


@login_required
def delete_course_employee(request, pk, cid):
    CourseEmployee.objects.filter(employee_id=pk, course_id=cid).delete()
    return redirect('view-course', cid)


@login_required
def delete_employee_course(request, pk, cid):
    CourseEmployee.objects.filter(course_id=pk, employee_id=cid).delete()
    return redirect('view-employee', cid)
