from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]


class LoginForm(AuthenticationForm):
    fields = ['username', 'password']


class PasswordChangeForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']


class PasswordResetForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']
