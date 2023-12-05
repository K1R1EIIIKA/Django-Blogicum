from django.urls import path, include

from . import views

urlpatterns = [
    path('login/',
         views.LoginUserView.as_view(), name='login'),
    path('registration/',
         views.RegistrationView.as_view(), name='registration'),
    path('password_reset/',
         views.PasswordResetUserView.as_view(), name='password_reset'),

    path('', include('django.contrib.auth.urls')),
]
