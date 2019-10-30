from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Raw_Data(models.Model):
    Charge_Station_Name = models.CharField(max_length=800)
    Session_Initiated_By = models.CharField(max_length=800)
    Start_Time = models.CharField(max_length=800)
     = models.CharField(max_length=800)