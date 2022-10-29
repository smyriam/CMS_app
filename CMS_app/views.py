from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from CMS_app.forms import AddEmployeeForm, AddCourse, EmployeeForm
from CMS_app.backend import Backend
from CMS_app.models import Employee, Course


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
    return render(request, "dashboard/dashboard.html", {"employees_count":employees_count, "courses_count":courses_count})


class add_employee_view(CreateView):
    template_name = 'employee/add_employee.html'
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('list-of-employees')


def add_employee(request):
    if request.method == "POST":
        form = AddEmployeeForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return JsonResponse({'msg': 'Data saved'})
        else:
            print("ERROR FORM INVALID")
            return JsonResponse({'msg': 'ERROR FORM INVALID'})
    else:
        form = AddEmployeeForm()
    return JsonResponse({'form': form})


class EmployeesList(ListView):
    template_name = 'employee/list_of_employees.html'
    model = Employee
    context_object_name = 'all_employees'


def delete_employee(request, pk):
    Employee.objects.filter(id=pk).delete()
    return redirect('list-of-employees')


class AddCourseView(CreateView):
    template_name = 'course/add_course.html'
    model = Course
    form_class = AddCourse
    success_url = reverse_lazy('list-of-courses')


class CoursesList(ListView):
    template_name = 'course/list_of_courses.html'
    model = Course
    context_object_name = 'all_courses'


def delete_course(request, pk):
    Course.objects.filter(id=pk).delete()
    return redirect('list-of-courses')


