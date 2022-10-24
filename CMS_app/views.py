from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from CMS_app.backend import Backend
from django.contrib import messages
from django.urls import reverse
from CMS_app.models import UserInstance


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

