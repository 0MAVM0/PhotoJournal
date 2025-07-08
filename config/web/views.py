from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import View

from .forms import RegisterForm


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
