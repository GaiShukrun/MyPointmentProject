from django.test import TestCase, tag, Client
from django.urls import reverse
from django.http import HttpRequest, HttpResponse,response,request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,get_user_model,get_user,user_logged_in
from .models import Appointment
import datetime


# The test john = Appointment.objects.get(<field>) for ex:
# john = Appointment.objects.get(day = "2022-12-18")
# is valid, because if we will insert in <field> other date and not what we did in setUp(self), so it will give error.
# EX: # john = Appointment.objects.get(day = "2022-12-25") - booking.models.Appointment.DoesNotExist: Appointment matching query does not exist.

class AppointmentTestCase(TestCase):
  def setUp(self):
    Appointment.objects.create(service = "Cardiologist" ,day = datetime.date(2022, 12, 18),time = "7:30 AM",syptoms = "Back pain")

  def test_appointment_service(self):
    john = Appointment.objects.get(service="Cardiologist")
    self.assertEqual(john.service, "Cardiologist")

  def test_appointment_day(self):
    john = Appointment.objects.get(day = "2022-12-18")
    self.assertEqual(john.day, datetime.date(2022, 12, 18))
    # self.assertNotEqual(john.day, datetime.date(2022, 12, 18))

  def test_appointment_time(self):
    john = Appointment.objects.get(time = "7:30 AM")
    self.assertNotEqual(john.time, "3:30 PM")
    self.assertEqual(john.time, "7:30 AM")

  def test_appointment_syptoms(self):
    # john = Appointment.objects.get(syptoms = "Leg pain")
    # This will give error because booking.models.Appointment.DoesNotExist: Appointment matching query does not exist.
    # so:
    john = Appointment.objects.get(syptoms = "Back pain")
    self.assertEqual(john.syptoms,"Back pain")
    
  def test_appointment_delete(self):
    # Create a test appointment
    appointment = Appointment.objects.create(id=150)
    
    # Checks if appointment.id == 150
    self.assertEqual(appointment.id,150)

    appointment.delete()

    # Checks if appointment with id 150 is deleted and is None
    self.assertEqual(appointment.id,None)


  def test_appointment_change_service(self):
    # Get a test appointment from setUp()
    app = Appointment.objects.get(service="Cardiologist")  

    # Checks if app.service == "Cardiologist"
    self.assertEqual(app.service,"Cardiologist")

    app.service = "Oncologist"

    # Checks if appointment.service really changed
    self.assertNotEqual(app.service,"Cardiologist")
    self.assertEqual(app.service,"Oncologist")
