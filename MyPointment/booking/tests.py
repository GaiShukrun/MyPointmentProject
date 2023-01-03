from django.test import TestCase, tag, Client
from django.urls import reverse
from django.http import HttpRequest, HttpResponse,response,request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,get_user_model,get_user,user_logged_in
from .models import Appointment
import datetime, unittest


# The test john = Appointment.objects.get(<field>) for ex:
# john = Appointment.objects.get(day = "2022-12-18")
# is valid, because if we will insert in <field> other date and not what we did in setUp(self), so it will give error.
# EX: # john = Appointment.objects.get(day = "2022-12-25") - booking.models.Appointment.DoesNotExist: Appointment matching query does not exist.

class AppointmentTestCase(TestCase):
  def setUp(self):
    Appointment.objects.create(service = "Cardiologist" ,day = datetime.date(2022, 12, 18),time = "7:30 AM",syptoms = "Back pain")
    Appointment.objects.create(service = "Oncologist" ,day = datetime.date(2022, 12, 17),time = "7:00 PM",syptoms = "pain")
    Appointment.objects.create(service = "Psychiatrist" ,day = datetime.date(2022, 12, 16),time = "6:00 PM",syptoms = "crazy crazy")
    Appointment.objects.create(service = "Neurologist", day = datetime.date(2022, 12, 15), time = "5:30 PM", syptoms = "migrane")

  def test_appointment_service(self):
    john = Appointment.objects.get(service="Cardiologist")
    self.assertEqual(john.service, "Cardiologist")
    Ron = Appointment.objects.get(service="Oncologist")
    self.assertEqual(Ron.service, "Oncologist")
    Din = Appointment.objects.get(service="Psychiatrist")
    self.assertEqual(Din.service, "Psychiatrist")
    Tal = Appointment.objects.get(service = "Neurologist")
    self.assertEqual(Tal.service, "Neurologist")
    

  def test_appointment_day(self):
    john = Appointment.objects.get(day = "2022-12-18")
    Ron = Appointment.objects.get(day = "2022-12-17")
    Din = Appointment.objects.get(day = "2022-12-16")
    Tal = Appointment.objects.get(day = "2022-12-15")
    self.assertEqual(john.day, datetime.date(2022, 12, 18))
    self.assertNotEqual(Ron.day, datetime.date(2022, 12, 18))
    self.assertEqual(Din.day, datetime.date(2022, 12, 16))
    self.assertEqual(Tal.day, datetime.date(2022, 12, 15))


  def test_appointment_time(self):
    john = Appointment.objects.get(time = "7:30 AM")
    Ron = Appointment.objects.get(time = "7:00 PM")
    Din = Appointment.objects.get(time = "6:00 PM")
    Tal = Appointment.objects.get(time = "5:30 PM")
    self.assertNotEqual(john.time, "3:30 PM")
    self.assertEqual(john.time, "7:30 AM")
    self.assertEqual(Ron.time, "7:00 PM")
    self.assertNotEqual(Din.time, "7:00 PM")
    self.assertNotEqual(Tal.time, "5:00 PM")


  def test_appointment_syptoms(self):
    # john = Appointment.objects.get(syptoms = "Leg pain")
    # This will give error because booking.models.Appointment.DoesNotExist: Appointment matching query does not exist.
    # so:
    john = Appointment.objects.get(syptoms = "Back pain")
    Ron = Appointment.objects.get(syptoms = "pain")
    Din = Appointment.objects.get(syptoms = "crazy crazy")
    Tal = Appointment.objects.get(syptoms = "migrane")
    self.assertEqual(john.syptoms,"Back pain")
    self.assertNotEqual(Ron.syptoms,"leg pain")
    self.assertEqual(Din.syptoms,"crazy crazy")
    self.assertEqual(Tal.syptoms,"migrane")