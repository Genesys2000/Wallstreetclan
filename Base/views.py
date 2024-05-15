# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import User, OTP, BlogPost
from .forms import CustomUserCreationForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')

def account(request):
    return render(request, 'account.html')

def blog(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'blog_posts': blog_posts})

def search(request):
    # Implement search functionality
    return render(request, 'search.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.terms_accepted = 'terms_accepted' in request.POST
            user.save()
            send_otp(user)
            return redirect('otp_verification')
    else:
        form = CustomUserCreationForm()
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
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            user = User.objects.filter(email=email, role=role).first()
            if user and user.check_password(password):
                send_otp(user)
                return redirect('otp_verification')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@csrf_exempt
def fingerprint_login(request):
    if request.method == 'POST':
        # Assuming fingerprint data is sent as JSON
        fingerprint_data = request.POST.get('fingerprint')
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user and authenticate_fingerprint(user, fingerprint_data):
            login(request, user)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failure'})

def authenticate_fingerprint(user, fingerprint_data):
    # Placeholder function for fingerprint authentication
    # Implement actual fingerprint authentication logic here
    return True


# Create your views here.
