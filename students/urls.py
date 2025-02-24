from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .decorators import redirect_authenticated_user

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', redirect_authenticated_user(auth_views.LoginView.as_view(template_name='students/login.html')), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('payment/initiate/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/success/', views.payment_success, name='payment_success'),
] 