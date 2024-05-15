# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    terms_accepted = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'terms_accepted']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
