from django.test import TestCase
from booking.models import Appointment
from django.contrib.auth.models import User
from django.urls import reverse

from fpdf import  FPDF
from Doctors import views
from django.http import HttpResponse,FileResponse


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

