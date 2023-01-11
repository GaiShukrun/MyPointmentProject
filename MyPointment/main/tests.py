from . import models, views, admin, forms
from django.test import TestCase, tag, Client
from django.urls import reverse
from django.core import mail
from django.http import HttpRequest, HttpResponse,response,request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,get_user_model,get_user,user_logged_in
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from booking.models import Appointment
# Create your tests here.

class SigninTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()
        self.user = get_user_model().objects.create_user(username='Oncologist', password='12test12', email='test@example.com')
        self.user.save()
        self.user = get_user_model().objects.create_user(username='Cardiologist', password='12test12', email='test@example.com')
        self.user.save()
        self.user = get_user_model().objects.create_user(username='Psychiatrist', password='12test12', email='test@example.com')
        self.user.save()
        self.user = get_user_model().objects.create_user(username='Neurologist', password='12test12', email='test@example.com')
        self.user.save()


    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_is_Oncologist(self):
        user = authenticate(username='Oncologist', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_is_Cardiologist(self):
        user = authenticate(username='Cardiologist', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)
        
    def test_is_Psychiatrist(self):
        user = authenticate(username='Psychiatrist', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_is_Neurologist(self):
        user = authenticate(username='Neurologist', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)
    
    def tearDown(self):
        self.user.delete()


class LoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)


    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
class PasswordResetRequestViewTest(TestCase):
    def test_password_reset_request(self):
    # Create a test user
        test_user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')

        # Send a POST request to the view function with a valid email
        response = self.client.post('/password_reset/', {'email': 'test@example.com'})

        # Check that the response is a redirect to the "password reset done" page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/password_reset/done/')

        # Check that an email was sent to the test user
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['test@example.com'])
class AvgTest(TestCase):
    def test_view_avg(self):
            # Create some test appointments
            appointment_1 = Appointment.objects.create(service='Cardiologist', Apperence=True, timetaken=30)
            appointment_2 = Appointment.objects.create(service='Oncologist', Apperence=False, timetaken=None)
            appointment_3 = Appointment.objects.create(service='Psychiatrist', Apperence=True, timetaken=45)
            appointment_4 = Appointment.objects.create(service='Neurologist', Apperence=True, timetaken=60)
            appointment_5 = Appointment.objects.create(service='Neurologist', Apperence=False, timetaken=None)
            
            # Issue a GET request to the view function
            response = self.client.get('/ViewAvg/')
            
            # Check that the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)
            
            # Check that the correct average values are returned
            #(<totalAvg>,<CardiologistAvg>,<OncologistAvg>,<PsychiatristAvg>,<NeurologistAvg>)
            self.assertEqual(response.context['avg'], (45, 30, 0, 45, 60))
            #(<totaNumAppointments>,<CardiologistNumAppointments>,<OncologistNumAppointments>,<PsychiatristNumAppointments>,<NeurologistNumAppointments>)
            self.assertEqual(response.context['NumberOfAppointment'], (5, 1, 1, 1, 2))
            #(<totalArrived>,<CardiologistArrived>,<OncologistArrived>,<PsychiatristArrived>,<NeurologistArrived>)
            self.assertEqual(response.context['NumberofAppointmentArrived'], (3, 1, 0, 1, 1))

class AdminSiteTests(TestCase):
   
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='testuser', password='testpass', email='test@example.com')
        self.client.login(username='testuser', password='testpass')

        # create a regular user for testing
        self.user = User.objects.create_user(username='testuser2', password='testpass2', email='test2@example.com',id=50)
    def test_change_user_fields(self):
        
        

        # send a request to the Django admin change form for the user
        response = self.client.get(f'/admin/auth/user/{50}/change/')
        self.assertEqual(response.status_code, 200)  # Check that the response is successful
        




        
        # send a request to the Django admin change form for the user
        response = self.client.get(f'/admin/auth/user/{50}/change/')
        self.assertEqual(response.status_code, 200)  # Checks that the response is successful