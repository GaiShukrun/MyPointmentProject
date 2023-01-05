from django.test import TestCase
from booking.models import Appointment
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from fpdf import  FPDF
from Doctors import views
from django.http import HttpResponse,FileResponse


class TestForDoctorApp(TestCase):
    def test_generatePDF(self):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='testpass')
        
        # Log the user in
        self.client.login(username='testuser', password='testpass')
        # Create some test appointments for the test user
        Appointment.objects.create(user=user, day=datetime.date(2022, 1, 1), time='09:00 AM', service='Cardiologist',id=50)
        app = Appointment.objects.get(id = 50)
        
        # Send a request to the generatePDF view
        response = self.client.get('/CardiologistApp/pdf/')
        
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

        
    def test_appointments_list(self):
        # Create a test user 

        user1 = User.objects.create_user(username='Cardiologist', password='testpass')
        
        # Log the user in
        self.client.login(username='Cardiologist', password='testpass')
        Appointment.objects.create(user=user1, day=datetime.date(2022, 1, 1), time='7:30 AM', service='Cardiologist', syptoms='chest pain',id=50)
        Appointment.objects.create(user=user1, day=datetime.date(2022, 5, 1), time='9:30 AM', service='Psychiatrist', syptoms='hair pain',id=51)
        Appointment.objects.create(user=user1, day=datetime.date(2022, 3, 1), time='10:30 AM', service='Neurologist', syptoms='finger pain',id=52)
        Appointment.objects.create(user=user1, day=datetime.date(2022, 2, 1), time='8:30 AM', service='Oncologist', syptoms='nose pain',id=53)
        
        
        response = self.client.get('/CardiologistApp/')
        self.assertEqual(response.status_code, 200)
        # Check that the rendered context contains the correct number of appointments
        self.assertEqual(len(response.context['App']), 4)



    def test_update_time(self):
        # Create a test user and log them in
        user1 = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create a test appointment for the test user
        appointment = Appointment.objects.create(user=user1, day='2022-01-01', time='09:00', service='Cardiologist', syptoms='chest pain', id=50)
        self.assertFalse(appointment.Apperence)
        # Send a POST request to the view function with a valid time taken
        response = self.client.post('/UpdateTime/50', {'username': '60'})
        self.assertEqual(response.status_code, 302)  # Check that the view function returns a redirect
        self.assertEqual(response['location'], '/CardiologistApp/')  # Check that the redirect URL is correct

        # Check that the appointment was updated correctly in the database
        updated_appointment = Appointment.objects.get(id=50)
        self.assertEqual(updated_appointment.timetaken, '60')
        self.assertTrue(updated_appointment.Apperence)