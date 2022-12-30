
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django import forms

SERVICE_CHOICES = (
    ("Cardiologist", "Cardiologist"),
    ("Oncologist", "Oncologist"),
    ("Psychiatrist", "Psychiatrist"),
    ("Neurologist", "Neurologist"),
    )
TIME_CHOICES = (
    ("7:30 AM", "7:30 AM"),
    ("8:00 AM", "8:00 AM"),
    ("8:30 AM", "8:30 AM"),
    ("9:00 AM", "9:00 AM"),
    ("9:30 AM", "9:30 AM"),
    ("10:00 AM", "10:00 AM"),
    ("10:30 AM", "10:30 AM"),
    ("11:00 AM", "11:00 AM"),
    ("11:30 AM", "11:30 AM"),
    ("12:00 PM", "12:00 PM"),
    ("12:30 PM", "12:30 PM"),
    ("1:00 PM", "1:00 PM"),
    ("1:30 PM", "1:30 PM"),
    ("2:00 PM", "2:00 PM"),
    ("2:30 PM", "2:30 PM"),
    ("3:00 PM", "3:00 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4:00 PM", "4:00 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5:00 PM", "5:00 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6:00 PM", "6:00 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7:00 PM", "7:00 PM"),
    ("7:30 PM", "7:30 PM"),
)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Cardiologist")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="7:30 AM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    syptoms = models.TextField(null=True, blank=True)
    timetaken = models.CharField(max_length=10,null=True, blank=True)
    Apperence = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"