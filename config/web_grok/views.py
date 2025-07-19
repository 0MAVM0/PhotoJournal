from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
import requests
import json

def get_api_data(endpoint, token=None):
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    response = requests.get(f'{settings.API_BASE_URL}{endpoint}', headers=headers)
    response.raise_for_status()
    return response.json()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('web:home')
    return render(request, 'web/login.html')

def register_view(request):
    return render(request, 'web/register.html')

@login_required
def home_view(request):
    token = request.session.get('access_token')
    posts = get_api_data('/posts/', token)
    return render(request, 'web/home.html', {'posts': posts})

@login_required
def profile_view(request, username):
    token = request.session.get('access_token')
    user = get_api_data(f'/users/{username}/', token)
    posts = get_api_data(f'/posts/?user__username={username}', token)
    followers = get_api_data(f'/follows/{username}/followers/', token)
    following = get_api_data(f'/follows/{username}/following/', token)
    return render(request, 'web/profile.html', {
        'profile_user': user,
        'posts': posts,
        'followers_count': len(followers),
        'following_count': len(following),
    })

@login_required
def post_detail_view(request, post_id):
    token = request.session.get('access_token')
    post = get_api_data(f'/posts/{post_id}/', token)
    comments = get_api_data(f'/posts/{post_id}/comments/', token)
    return render(request, 'web/post_detail.html', {'post': post, 'comments': comments})
