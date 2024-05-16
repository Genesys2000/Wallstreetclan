# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Property, Offer

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

class PropertyTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='testuser@example.com', password='password123', role='buyer')
        self.property = Property.objects.create(owner=self.user, title='Test Property', description='A test property', location='Test Location', price=100000.00)

    def test_property_list_view(self):
        response = self.client.get(reverse('property_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property')

    def test_property_detail_view(self):
        response = self.client.get(reverse('property_detail', args=[self.property.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property')

    def test_make_offer_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('make_offer', args=[self.property.pk]), {'offer_price': 95000.00})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Offer.objects.filter(property=self.property, buyer=self.user, offer_price=95000.00).exists())


# Create your tests here.
