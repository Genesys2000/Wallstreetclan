# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class UserRegistrationTest(TestCase):
    def test_registration_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'role': 'buyer',
            'terms_accepted': True,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(get_user_model().objects.filter(email='testuser@example.com').exists())

    def test_otp_sent_on_registration(self):
        self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'role': 'buyer',
            'terms_accepted': True,
        })
        user = get_user_model().objects.get(email='testuser@example.com')
        self.assertTrue(OTP.objects.filter(user=user).exists())



# Create your tests here.
