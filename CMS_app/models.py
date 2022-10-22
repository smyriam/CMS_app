from django.db import models


# Create your models here.
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = (('intern', 'Intern'), ('extern', 'Extern'))
    location_details = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    participation_fee = models.IntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Division(models.Model):
    id = models.AutoField(primary_key=True)
    structure = (('central', 'Central'), ('regional', 'Regional'))
    division_name = models.CharField(max_length=64)
    objects = models.Manager()


class Funding(models.Model):
    id = models.AutoField(primary_key=True)
    structure = (('proprii', 'Fonduri proprii'), ('altele', 'Alte fonduri'))
    substructure = models.CharField(max_length=64)
    objects = models.Manager()


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128)
    structure = (('central', 'Central'), ('regional', 'Regional'))
    division_id = models.ForeignKey(Division, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class CourseEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    source_of_funding = models.ForeignKey(Funding, on_delete=models.DO_NOTHING)
    transport_costs = models.IntegerField()
    accomodation_costs = models.IntegerField()
    allowance_costs = models.IntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance_id = models.ForeignKey(CourseEmployee, on_delete=models.CASCADE)
    survey_link = models.CharField(max_length=255)
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
