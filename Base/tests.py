# tests.py
from django.test import TestCase
from django.urls import reverse
from .models import User, OTP

class HomeViewTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

class RegisterViewTests(TestCase):
    def test_register_view_status_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

class LoginViewTests(TestCase):
    def test_login_view_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

class OTPVerificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
        self.otp = OTP.objects.create(user=self.user, otp='123456')

    def test_otp_verification_view_status_code(self):
        response = self.client.get(reverse('otp_verification'))
        self.assertEqual(response.status_code, 200)

    def test_otp_is_valid(self):
        self.assertTrue(self.otp.is_valid())


# Create your tests here.
