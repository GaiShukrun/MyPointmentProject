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


  def test_user_panel(self):
      # Create a test user
      user = User.objects.create_user(username='testuser', password='testpass')
      # Log the user in
      self.client.login(username='testuser', password='testpass')
       # Create an appointment for the test user
      appointment = Appointment.objects.create(user=user, day='2022-01-01', time='09:00', service='Cardiologist')
      # Get the URL for the userPanel view
      url = reverse('userPanel')
    # Send a GET request to the userPanel view
      response = self.client.get(url)
    # Assert that the response status code is 200 (OK)
      self.assertEqual(response.status_code, 200)
    # Assert that the response status code is not 404 (Not Found)
      self.assertNotEqual(response.status_code, 404)
    # Assert that the user and appointments variables are passed to the template
      self.assertIn('user', response.context)
      self.assertIn('appointments', response.context)
    # Assert that the correct user and appointments are passed to the template
      self.assertEqual(response.context['user'], user)
      




  