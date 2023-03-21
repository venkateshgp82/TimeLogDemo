from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    project_id = models.CharField(max_length=25, unique=True)

class Timelog(models.Model):
    work_hours = models.DecimalField(max_digits=5, decimal_places=2)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=8) #Date format is YYYYMMDD

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
