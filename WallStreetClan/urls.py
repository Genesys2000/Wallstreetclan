"""
URL configuration for WallStreetClan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py
from django.urls import path
from Base.views import home, about_us, account, blog, search, register, otp_verification, user_login, user_logout, fingerprint_login, property_list, property_detail, make_offer

urlpatterns = [
    path('', home, name='home'),
    path('about/', about_us, name='about_us'),
    path('account/', account, name='account'),
    path('blog/', blog, name='blog'),
    path('search/', search, name='search'),
    path('register/', register, name='register'),
    path('otp_verification/', otp_verification, name='otp_verification'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('properties/', property_list, name='property_list'),
    path('properties/<int:pk>/', property_detail, name='property_detail'),
    path('properties/<int:pk>/make_offer/', make_offer, name='make_offer'),
    path('fingerprint_login/', fingerprint_login, name='fingerprint_login'),
]


    

