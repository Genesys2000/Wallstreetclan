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


# Create your models here.
