from django.contrib import admin

from CMS_app.models import Employee, Course, CourseEmployee, Division, Funding, Structure

# Register your models here.

admin.site.register(Employee)
admin.site.register(Course)
admin.site.register(CourseEmployee)
admin.site.register(Funding)
admin.site.register(Structure)
admin.site.register(Division)
