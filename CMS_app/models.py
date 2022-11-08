from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class UserInstance(User):
    user_types = [(1, "Admin"), (2, "Employee")]
    user_type = models.CharField(default=1, choices=user_types, max_length=1)


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
    location_options =[('1', 'Intern'), ('2', 'Extern')]
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(choices=location_options, max_length=1)
    location_details = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    participation_fee = models.IntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.course_name}'


class Structure(models.Model):
    structure = models.CharField(max_length=8)

    def __str__(self):
        return self.structure


class Division(models.Model):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    division = models.CharField(max_length=64)

    def __str__(self):
        return self.division


class FundStruct(models.Model):
    id = models.AutoField(primary_key=True)
    structure_name = models.CharField(max_length=32)
    objects = models.Manager()


class Funding(models.Model):
    id = models.AutoField(primary_key=True)
    structure = models.ForeignKey(FundStruct, on_delete=models.DO_NOTHING)
    substructure = models.CharField(max_length=64)
    objects = models.Manager()

    def __str__(self):
        return f'{self.substructure}'


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(blank=True, max_length=128)
    structure = models.ForeignKey(Structure, on_delete=models.SET_NULL, blank=True, null=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ["last_name"]

class CourseEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    duration = models.IntegerField(blank=True)
    source_of_funding = models.ForeignKey(Funding, on_delete=models.DO_NOTHING, blank=True)
    transport_costs = models.IntegerField(blank=True)
    accommodation_costs = models.IntegerField(blank=True)
    allowance_costs = models.IntegerField(blank=True)
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
