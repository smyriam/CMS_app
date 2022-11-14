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

                  path('employees', views.EmployeesList.as_view(), name='list-of-employees'),
                  path('employees/add/', views.add_employee, name='add-employee'),
                  path('employees/<int:pk>/edit/', views.edit_employee, name='edit-employee'),
                  path('employees/ajax/load-divisions', views.load_divisions, name='ajax_load_divisions'),
                  path('employees/<int:pk>/', views.EmployeeDetailsView.as_view(), name='view-employee'),
                  path('employees/<int:pk>/delete/', views.delete_employee, name='delete-employee'),

                  path('courses', views.CoursesList.as_view(), name='list-of-courses'),
                  path('courses/add/', views.add_course, name='add-course'),
                  path('courses/<int:pk>/edit/', views.edit_course, name='edit-course'),
                  path('courses/<int:pk>/delete/', views.delete_course, name='delete-course'),
                  path('courses/<int:pk>/', views.CourseDetailsView.as_view(), name='view-course'),

                  path('course_employee/<int:pk>/add_course/', views.assign_course, name='assign-course'),
                  path('course_employee/<int:pk>/add_employee/', views.assign_employee, name='assign-employee'),
                  path('course_employee/<int:pk>/<int:cid>/edit/', views.edit_assign, name='edit-assign'),
                  path('course_employee/ajax/load-fundings', views.load_fundings, name='ajax_load_funding'),

                  path('course_employee/<int:pk>/<int:cid>/delete/', views.delete_course_employee, name='delete-course-employee'),
                  path('employee_course/<int:pk>/<int:cid>/delete/', views.delete_employee_course, name='delete-employee-course'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
