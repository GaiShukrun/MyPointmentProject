from django.test import TestCase
from models import Appointment

class AppointmentTestCase(TestCase):
  def setUp(self):
    Appointment.objects.create(name="John Doe", time="2022-12-15 14:30:00")
    Appointment.objects.create(name="Jane Smith", time="2022-12-16 10:00:00")
    
  def test_appointment_name(self):
    john = Appointment.objects.get(name="John Doe")
    jane = Appointment.objects.get(name="Jane Smith")
    self.assertEqual(john.name, "John Doe")
    self.assertEqual(jane.name, "Jane Smith")
    
  def test_appointment_time(self):
    john = Appointment.objects.get(name="John Doe")
    jane = Appointment.objects.get(name="Jane Smith")
    self.assertEqual(john.time, "2022-12-15 14:30:00")
    self.assertEqual(jane.time, "2022-12-16 10:00:00")