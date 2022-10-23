from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from CMS_app.backend import Backend

# Create your views here.
def ShowTestPage(request):
    return render(request,"test.html")

def ShowLoginPage(request):
    return render(request,"login.html")

def Login(request):
    if request.method != "POST":
        return HttpResponse("<h2>Not allowed</h2>")
    else:
        user = Backend.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request,user)
            return HttpResponse("Email : " +request.POST.get("email") + " Password : " +request.POST.get("password"))
        else:
            return HttpResponse("Invalid login")


def UserDetails(request):
    if request.user != None:
        return HttpResponse("User : " +request.user.email + "Type : " + str(request.user.user_type))
    else:
        return HttpResponse("Please, login first")


def Logout(request):
    logout(request)
    return HttpResponseRedirect("/")