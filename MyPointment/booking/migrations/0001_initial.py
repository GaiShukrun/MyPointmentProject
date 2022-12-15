# Generated by Django 4.0 on 2022-12-15 16:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Oncologist', 'Oncologist'), ('Psychiatrist', 'Psychiatrist'), ('Neurologist', 'Neurologist')], default='Cardiologist', max_length=50)),
                ('day', models.DateField(default=datetime.datetime.now)),
                ('time', models.CharField(choices=[("7:30 AM", "7:30 AM"),("8:00 AM", "8:00 AM"),("8:30 AM", "8:30 AM"),
                ("9:00 AM", "9:00 AM"),("9:30 AM", "9:30 AM"),("10:00 AM", "10:00 AM"),("10:30 AM", "10:30 AM"),("11:00 AM", "11:00 AM"),("11:30 AM", "11:30 AM"),("12:00 PM", "12:00 PM"),("12:30 PM", "12:30 PM"),("1:00 PM", "1:00 PM"),("1:30 PM", "1:30 PM"),("2:00 PM", "2:00 PM"),("2:30 PM", "2:30 PM"),('3:00 PM', '3:00 PM'), ('3:30 PM', '3:30 PM'), ('4:00 PM', '4:00 PM'), ('4:30 PM', '4:30 PM'), ('5:00 PM', '5:00 PM'), ('5:30 PM', '5:30 PM'), ('6:00 PM', '6:00 PM'), ('6:30 PM', '6:30 PM'), ('7:00 PM', '7:00 PM'), ('7:30 PM', '7:30 PM')], default='7:30 AM', max_length=10)),
                ('time_ordered', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
