"""CMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from CMS import settings
from CMS_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_login_page, name='login'),
    path('home', views.admin_home, name='admin-home'),
    path('login', views.do_login),
    path('logout', views.do_logout, name='logout'),
    path('user_details', views.user_details),
    path('reset_password', views.reset_password, name='reset-password'),
    path('employees/add_form', views.AddEmployeeView.as_view(), name='add-employee'),
    path('employees/add', views.add_employee, name='add-new-employee'),
    path('employees', views.EmployeesList.as_view(), name='list-of-employees'),
    path('employees/<int:pk>/', views.EmployeeDetailsView.as_view(), name='view-employee'),
    path('employees/<int:pk>/delete/', views.delete_employee, name='delete-employee'),
    path('courses/add', views.AddCourseView.as_view(), name='add-course'),
    path('courses', views.CoursesList.as_view(), name='list-of-courses'),
    path('courses/<int:pk>/delete/', views.delete_course, name='delete-course'),
    path('courses/<int:pk>/view/', views.CourseDetailsView.as_view(), name='view-course'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
