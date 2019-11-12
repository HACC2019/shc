import csv
import os

from Front.models import Raw_Data # imports the model
def csv():
    with open('Data_HACC.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p = Raw_Data(Charge_Station_Name=row['Charge Station Name'], Session_Initiated_By=row['Session Initiated By'], Start_Time=row['Start Time'], End_Time=row['End Time'], Duration=row['Duration'], Energy=row['Energy(kWh)'], Session_Amount=row['Session Amount'], Session_Id=row['Session Id'], Port_Type=row['Port Type'], Payment_Mode=row['Payment Mode'])
            p.save()
    exit()