from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Subquery
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from posts.models import Post
from posts.forms import PostCreateForm
from users.forms import UserUpdateForm
from users.models import CustomUser
from comments.models import Comment
from likes.models import Like
from .forms import RegisterForm, PostEditForm


@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.select_related('user').prefetch_related('likes', 'comments').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        liked_ids = set(user.likes.values_list('post_id', flat=True)) if user.is_authenticated else set()

        for post in context['posts']:
            post.is_liked_by_me = post.id in liked_ids
            post.likes_count = post.likes.count()
            post.comments_count = post.comments.count()

        return context


class RegisterPageView(View):
    def get(self, request):
        return render(request, 'register.html', {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('home')

        messages.error(request, 'Please fix the errors below.')
        return render(request, 'register.html', {'form': form})


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

@require_POST
def ajax_like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    like = Like.objects.filter(user=user, post=post).first()
    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(user=user, post=post)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })

@require_POST
def ajax_comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content', '').strip()

    if content:
        comment = Comment.objects.create(post=post, user=request.user, content=content)
        return JsonResponse({
            'user': request.user.username,
            'content': comment.content,
            'created': comment.created_at.strftime('%Y-%m-%d %H:%M'),
            'comments_count': post.comments.count(),
        })

    return JsonResponse({'error': 'Empty content'}, status=400)

@method_decorator(login_required, name='dispatch')
class DeletePostView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.user != request.user:
            messages.error(request, 'You do not have permission to delete this post.')
        else:
            post.delete()
            messages.success(request, 'Post deleted successfully.')
        return redirect('home')


class EditPostView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.user != request.user:
            messages.error(request, "You cannot edit this post.")
            return redirect('home')
        return render(request, 'edit_post.html', {'form': PostEditForm(instance=post), 'post': post})

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


class ProfileView(View):
    def get(self, request, username):
        profile_user = get_object_or_404(CustomUser, username=username)
        posts = Post.objects.filter(user=profile_user).order_by('-created_at')\
            .prefetch_related('comments', 'likes')

        for post in posts:
            post.is_liked_by_me = post.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
            post.likes_count = post.likes.count()
            post.comment_count = post.comments.count()

        return render(request, 'profile.html', {'profile_user': profile_user, 'posts': posts})


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request):
        return render(request, 'edit_profile.html', {'form': UserUpdateForm(instance=request.user)})

    def post(self, request):
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile', username=request.user.username)
        messages.error(request, 'Please correct the errors below.')
        return render(request, 'edit_profile.html', {'form': form})


class LikedPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'liked_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        liked_ids = Like.objects.filter(user=self.request.user).values('post_id')
        return Post.objects.filter(id__in=Subquery(liked_ids)).select_related('user').prefetch_related('comments')


class UserSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        users = CustomUser.objects.filter(username__icontains=query) if query else CustomUser.objects.all()
        return render(request, 'user_search.html', {'users': users, 'query': query})
