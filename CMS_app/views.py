from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from CMS_app.forms import AddEmployee, AddCourse, EmployeeForm
from CMS_app.backend import Backend
from CMS_app.models import Employee, Course, Division
from django import forms


# Create your views here.
def ShowTestPage(request):
    return render(request, "test.html")


def ShowBase(request):
    return render(request, "base.html")


def ShowLoginPage(request):
    return render(request, "login.html")


def doLogin(request):
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


def UserDetails(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email)
    else:
        return HttpResponse("Please, login first")


def doLogout(request):
    logout(request)
    return HttpResponseRedirect("/")


def AdminHome(request):
    return render(request, "base.html")


class AddEmployeeView(CreateView):
    template_name = 'employee/add_employee.html'
    model = Employee
    form_class = AddEmployee
    success_url = reverse_lazy('list-of-employees')


class EmployeesList(ListView):
    template_name = 'employee/list_of_employees.html'
    model = Employee
    context_object_name = 'all_employees'


def DeleteEmployee(request, pk):
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


def DeleteCourse(request, pk):
    Course.objects.filter(id=pk).delete()
    return redirect('list-of-courses')


