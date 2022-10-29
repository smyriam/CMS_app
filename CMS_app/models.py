from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class UserInstance(User):
    user_types = [(1, "Admin"), (2, "Employee")]
    user_type = models.CharField(default=1, choices=user_types, max_length=8)


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
    location_options =[('intern', 'Intern'), ('extern', 'Extern')]
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(choices=location_options, max_length=6)
    location_details = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    participation_fee = models.IntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.course_name}'

class Division(models.Model):
    structure_options = [('central', 'Central'), ('regional', 'Regional')]
    id = models.AutoField(primary_key=True)
    structure = models.CharField(choices=structure_options, max_length=8)
    division_name = models.CharField(max_length=64)
    objects = models.Manager()

    def __str__(self):
        return f'{self.division_name}'


class Funding(models.Model):
    id = models.AutoField(primary_key=True)
    structure_options = [('proprii', 'Fonduri proprii'), ('altele', 'Alte fonduri')]
    substructure = models.CharField(max_length=64)
    objects = models.Manager()


class Employee(models.Model):
    structure_options = [('central', 'Central'), ('regional', 'Regional')]
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(blank=True, max_length=128)
    structure = models.CharField(choices=structure_options, max_length=8)
    division = models.ForeignKey(Division, on_delete=models.DO_NOTHING, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.first_name}{self.last_name}'

    class Meta:
        ordering = ["last_name"]

class CourseEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    duration = models.IntegerField()
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


@receiver(post_save, sender = UserInstance)
def create_admin(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Employee.objects.create(admin=instance)

@receiver(post_save, sender = UserInstance)
def save_admin(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.employee.save()