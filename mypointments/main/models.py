from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    secure_question = models.CharField(validators=[MinLengthValidator(2)],max_length=50)
    secure_answer = models.CharField(validators=[MinLengthValidator(2)],max_length=50)
    is_doctor = models.BooleanField()

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    docType = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)

