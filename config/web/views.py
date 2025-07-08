from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import View

from .forms import RegisterForm
from posts.models import Post


class RegisterPageView(View):
    def get(self, request):
        form = RegisterForm()

        return render(request, 'register.html', { 'form': form })

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'You have successfully registered!')

            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')

        return render(request, 'register.html', { 'form': form })


class LoginPageView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

    def get_success_url(self):
        return redirect('home')
