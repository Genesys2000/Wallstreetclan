# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import User, OTP

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_otp(user)
            return redirect('otp_verification')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def send_otp(user):
    otp_code = get_random_string(length=6, allowed_chars='0123456789')
    OTP.objects.create(user=user, otp=otp_code)
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp_code}',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )

def otp_verification(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        otp = OTP.objects.filter(otp=otp_code, user__email=request.POST.get('email')).first()
        if otp and otp.is_valid():
            otp.is_used = True
            otp.save()
            login(request, otp.user)
            return redirect('home')
    return render(request, 'otp_verification.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            send_otp(user)
            return redirect('otp_verification')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')


# Create your views here.
