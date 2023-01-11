from django.test import TestCase, tag, Client
from django.urls import reverse
from django.http import HttpRequest, HttpResponse,response,request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,get_user_model,get_user,user_logged_in
from .models import Appointment
import datetime
from django.http import HttpResponse,FileResponse
from fpdf import  FPDF


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
    john = Appointment.objects.get(syptoms = "Back pain")
    Ron = Appointment.objects.get(syptoms = "pain")
    Din = Appointment.objects.get(syptoms = "crazy crazy")
    Tal = Appointment.objects.get(syptoms = "migrane")
    self.assertEqual(john.syptoms,"Back pain")
    self.assertNotEqual(Ron.syptoms,"leg pain")
    self.assertEqual(Din.syptoms,"crazy crazy")
    self.assertEqual(Tal.syptoms,"migrane")

class AppointmentEmailSent(TestCase):
  def setUp(self):
    self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
    self.user.save()


  def test_email(self):
    subject = "test"
    email = "admin@example.com"
    mail.send_mail(subject, email, 'admin@example.com' , [User.email], fail_silently=False)
    self.assertEqual(len(mail.outbox),1)
    self.assertEqual(mail.outbox[0].subject, "test")
    self.assertEqual(mail.outbox[0].to, [User.email])
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
      

class TestGeneratePDF(TestCase):
    def test_generatePDF(self):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='testpass')
        
        # Log the user in
        self.client.login(username='testuser', password='testpass')
        # Create some test appointments for the test user
        Appointment.objects.create(user=user, day='2022-01-01', time='09:00', service='Cardiology',id=50)
        app = Appointment.objects.get(id = 50)
        
        # Send a request to the generatePDF view
        response = self.client.get('/user-panel/pdf/')
        
        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Check that the response content-type is 'application/pdf'
        self.assertEqual(response['Content-Type'], 'application/pdf')
        # Check that the response is a FileResponse
        self.assertIsInstance(response, FileResponse)
        
        # Check that the PDF file was created and is being served correctly
        with open('report.pdf', 'rb') as pdf_file:
         for chunk in response.streaming_content:
            self.assertEqual(chunk, pdf_file.read(len(chunk)))
         self.assertEqual(pdf_file.read(), b'')


