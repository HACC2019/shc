# Generated by Django 2.2.6 on 2019-11-10 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Front', '0003_remove_raw_data_payment_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='raw_data',
            name='Payment_Mode',
            field=models.CharField(default='null', max_length=800),
            preserve_default=False,
        ),
    ]
