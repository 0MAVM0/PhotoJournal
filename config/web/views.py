from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View

from .forms import RegisterForm, PostEditForm
from posts.forms import PostCreateForm
from comments.models import Comment
from posts.models import Post


@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.select_related('user').prefetch_related('likes', 'comments').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for post in context['posts']:
            post.is_liked_by_me = post.likes.filter(user=self.request.user).exists()
        return context


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


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')

    if content:
        Comment.objects.create(
            user=request.user,
            post=post,
            content=content
        )
        messages.success(request, 'Comment added.')
    else:
        messages.error(request, 'Comment cannot be empty.')
    return redirect('home')


@method_decorator(login_required, name='dispatch')
class DeletePostView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.user != request.user:
            messages.error(request, 'You do not have permission to delete this post.')
            return redirect('home')
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('home')


class EditPostView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.user != request.user:
            messages.error(request, "You cannot edit this post.")
            return redirect('home')
        form = PostEditForm(instance=post)
        return render(request, 'edit_post.html', {'form': form, 'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.user != request.user:
            messages.error(request, "You cannot edit this post.")
            return redirect('home')
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect('home')
        return render(request, 'edit_post.html', {'form': form, 'post': post})
