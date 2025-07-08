from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View

from posts.forms import PostCreateForm
from .forms import RegisterForm
from posts.models import Post


@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.select_related('user').prefetch_related('likes', 'comments').order_by('-created_at')


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
        return reverse_lazy('home')


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'create_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
