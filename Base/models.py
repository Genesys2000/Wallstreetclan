# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('realtor', 'Realtor'),
        ('property_owner', 'Property Owner'),
        ('group_manager', 'Group Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    terms_accepted = models.BooleanField(default=False)

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # OTP is valid for 10 minutes
        return (timezone.now() - self.created_at).seconds < 600 and not self.is_used

class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    listed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Offer(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='offers')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"{self.property.title} - {self.offer_price}"

# Create your models here.
