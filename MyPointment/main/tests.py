from . import models, views, admin, forms
from django.test import TestCase, tag, Client
from django.urls import reverse
from django.http import HttpRequest, HttpResponse,response,request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,get_user_model,get_user,user_logged_in
from django.test import TestCase
from django.urls import reverse
from django.core import mail

# Create your tests here.

class SigninTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
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


    



        