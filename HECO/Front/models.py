from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Raw_Data(models.Model):
    Charge_Station_Name = models.CharField(max_length=800)
    Session_Initiated_By = models.CharField(max_length=800)
    Start_Time = models.CharField(max_length=800)
    End_Time = models.CharField(max_length=800)
    Duration = models.CharField(max_length=800)
    Energy = models.CharField(max_length=800)
    Session_Amount = models.CharField(max_length=800)
    Session_Id = models.CharField(max_length=800)
    Port_Type = models.CharField(max_length=800)
    Payment_Mode = models.CharField(max_length=800)

    def __str__(self):
        return self.Charge_Station_Name

