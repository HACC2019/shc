# Generated by Django 2.2.6 on 2019-11-06 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Front', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='procc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unix_time_stamp', models.CharField(max_length=800)),
                ('Charge_Station_Name', models.CharField(max_length=800)),
                ('Average_kwh', models.CharField(max_length=800)),
            ],
        ),
    ]
