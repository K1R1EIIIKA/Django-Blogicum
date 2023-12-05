from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import (LoginForm,
                    RegistrationForm,
                    PasswordResetForm)


class LoginUserView(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse('blog:index')


class RegistrationView(View):
    page_name = 'registration'
    template_name = 'registration/registration_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:index')

        form = RegistrationForm()

        return render(request, self.template_name,
                      {
                          'page_name': self.page_name,
                          'form': form
                      })

    def post(self, request):
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password1 = request.POST.get('password1')

            user = authenticate(username=username, password=password1)
            login(request, user)

            return redirect('blog:index')

        return render(request, self.template_name,
                      {
                          'page_name': self.page_name,
                          'form': form
                      })


class PasswordResetUserView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        send_mail(
            f'Сброс пароля почты {form.cleaned_data["email"]}',
            'Ссылка для сброса пароля',
            'asaaa@gmail.com',
            [form.cleaned_data['email']],
            fail_silently=False,
        )

        return render(self.request, 'registration/password_reset_done.html')
