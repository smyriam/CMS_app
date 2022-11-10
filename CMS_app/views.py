from django.contrib.auth import login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from CMS_app.forms import AddEmployeeForm, AddCourseForm, EditEmployeeForm, EditCourseForm, AssignCourseForm, \
    AssignEmployeeForm
from CMS_app.backend import Backend
from CMS_app.models import Employee, Course, CourseEmployee, Division, Funding


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


def user_details(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email)
    else:
        return HttpResponse("Please, login first")


def do_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def reset_password(request):
    return render(request, "reset_password.html")


def admin_home(request):
    employees_count = Employee.objects.all().count()
    courses_count = Course.objects.all().count()
    return render(request, "dashboard/dashboard.html",
                  {"employees_count": employees_count, "courses_count": courses_count})


class EmployeeDetailsView(DetailView):
    template_name = 'employee/employee_details.html'
    model = Employee

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        selects = CourseEmployee.objects.filter(employee_id=self.kwargs['pk']).all()
        courses = []
        for i in selects:
            courses.append(Course.objects.filter(id=i.course_id).first())
        data['courses'] = courses
        return data

#
# class EmployeeAddCourse(DetailView):
#     template_name = 'employee/select_course.html'
#     model = Employee
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#
#         exclude = CourseEmployee.objects.filter(employee_id=self.kwargs['pk']).all()
#         all_courses = Course.objects.filter(active=True).all()
#         if exclude.count() == 0:
#             courses = []
#             for i in all_courses:
#                 courses.append(Course.objects.filter(id=i.id).first())
#
#         data['courses'] = courses
#         return data


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


def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EditEmployeeForm(instance=employee)
    if request.method == 'POST':
        form = EditEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('list-of-employees')
    return render(request, 'employee/edit_employee_template.html', {'form': form})


def load_divisions(request):
    structure_id = request.GET.get('structure_id')
    divisions = Division.objects.filter(structure_id=structure_id).all()
    return render(request, 'employee/division_options.html', {'divisions': divisions})


# def edit_employee(request, employee_id):
#     employee = Employee.objects.get(id=employee_id)
#     form = EditEmployeeForm()
#     form.fields['first_name'].initial = employee.first_name
#     form.fields['last_name'].initial = employee.last_name
#     form.fields['email'].initial = employee.email
#     form.fields['structure'].initial = employee.structure
#     form.fields['division'].initial = employee.division
#     form.fields['active'].initial = employee.active
#     return render(request, 'employee/edit_employee_template.html',
#                   {'form': form, "first_name": employee.first_name, "last_name": employee.last_name })


def edit_employee_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        employee_id = request.session.get("employee_id")
        if employee_id == None:
            return HttpResponseRedirect(reverse('list-of-employees'))

        form = EditEmployeeForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            structure = form.cleaned_data['structure']
            division = form.cleaned_data['division']
            active = form.cleaned_data['active']

            try:
                employee = Employee.objects.get(id=employee_id)
                employee.first_name = first_name
                employee.last_name = last_name
                employee.email = email
                employee.structure = structure
                employee.division = Division.objects.get(id=division)
                employee.active = active
                employee.save(commit=True)
                
                messages.success(request, "Successfully Edited Employee")
                return HttpResponseRedirect(reverse('list-of-employees'))
            except:
                messages.error(request, "Failed to Edit Employee")
                return HttpResponseRedirect(reverse('list-of-employees'))
        else:
            form = EditEmployeeForm(request.POST)
            employee = Employee.objects.get(id=employee_id)
            return render(request, 'employee/edit_employee_template.html',
                          {"form": form, 'first_name': employee.first_name, 'last_name': employee.last_name })


class EmployeesList(ListView):
    template_name = 'employee/list_of_employees.html'
    model = Employee
    context_object_name = 'all_employees'


def delete_employee(request, pk):
    Employee.objects.filter(id=pk).delete()
    return redirect('list-of-employees')


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


def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = EditCourseForm(instance=course)
    if request.method == 'POST':
        form = EditCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('list-of-courses')
    return render(request, 'course/edit_course_template.html', {'form': form})


class CoursesList(ListView):
    template_name = 'course/list_of_courses.html'
    model = Course
    context_object_name = 'all_courses'


def delete_course(request, pk):
    Course.objects.filter(id=pk).delete()
    return redirect('list-of-courses')


class CourseDetailsView(DetailView):
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
            return redirect('view-employee', pk)
    return render(request, 'employee/assign_course_template.html', {'form': form, 'first_name': employee_data.first_name, 'last_name': employee_data.last_name })


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
            return redirect('view-course', pk)
    return render(request, 'course/assign_employee_template.html', {'form': form, 'course_name': course_data.course_name })


def load_fundings(request):
    structure_id = request.GET.get('structure_id')
    divisions = Funding.objects.filter(structure_id=structure_id).all()
    return render(request, 'employee/division_options.html', {'divisions': divisions})


def delete_course_employee(request, pk, cid):
    CourseEmployee.objects.filter(employee_id=pk, course_id=cid).delete()
    return redirect('view-course', cid)


def delete_employee_course(request, pk, cid):
    CourseEmployee.objects.filter(course_id=pk, employee_id=cid).delete()
    return redirect('view-employee', cid)

