from django.shortcuts import render

# Create your views here.
def ShowTestPage(request):
    return render(request,"test.html")