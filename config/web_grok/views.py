from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
import json

def get_api_data(endpoint, token=None):
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    try:
        response = requests.get(f'{settings.API_BASE_URL}{endpoint}', headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []

def login_view(request):
    if request.user.is_authenticated:
        return redirect('web:home')
    if request.method == 'POST':
        try:
            response = requests.post(f'{settings.API_BASE_URL}users/login/', data=request.POST)
            if response.status_code == 200:
                data = response.json()
                request.session['access_token'] = data['access']
                return redirect('web:home')
        except requests.RequestException:
            return render(request, 'web/login.html', {'error': 'Invalid credentials'})
    return render(request, 'web/login.html')

def register_view(request):
    if request.method == 'POST':
        try:
            response = requests.post(f'{settings.API_BASE_URL}users/register/', data=request.POST)
            if response.status_code == 201:
                data = response.json()
                request.session['access_token'] = data['access']
                return redirect('web:home')
            else:
                return render(request, 'web/register.html', {'error': response.json().get('detail', 'Registration failed')})
        except requests.RequestException:
            return render(request, 'web/register.html', {'error': 'Registration failed'})
    return render(request, 'web/register.html')

def home_view(request):
    token = request.session.get('access_token') if request.user.is_authenticated else None
    posts = get_api_data('posts/', token)
    return render(request, 'web/home.html', {'posts': posts})

@login_required
def profile_view(request, username):
    token = request.session.get('access_token')
    user = get_api_data(f'users/{username}/', token)
    posts = get_api_data(f'posts/?user__username={username}', token)
    followers = get_api_data(f'follows/{username}/followers/', token)
    following = get_api_data(f'follows/{username}/following/', token)
    return render(request, 'web/profile.html', {
        'profile_user': user,
        'posts': posts,
        'followers_count': len(followers),
        'following_count': len(following),
    })

@login_required
def post_detail_view(request, post_id):
    token = request.session.get('access_token')
    post = get_api_data(f'posts/{post_id}/', token)
    comments = get_api_data(f'posts/{post_id}/comments/', token)
    return render(request, 'web/post_detail.html', {'post': post, 'comments': comments})

@login_required
def chats_view(request):
    token = request.session.get('access_token')
    chats = get_api_data('chats/', token)
    return render(request, 'web/chats.html', {'chats': chats})

@login_required
def chat_detail_view(request, chat_id):
    token = request.session.get('access_token')
    chat = get_api_data(f'chats/{chat_id}/', token)
    return render(request, 'web/chat_detail.html', {'chat': chat})

@login_required
def followers_view(request, username):
    token = request.session.get('access_token')
    followers = get_api_data(f'follows/{username}/followers/', token)
    return render(request, 'web/followers.html', {'users': followers, 'title': f"{username}'s Followers"})

@login_required
def following_view(request, username):
    token = request.session.get('access_token')
    following = get_api_data(f'follows/{username}/following/', token)
    return render(request, 'web/following.html', {'users': following, 'title': f"{username}'s Following"})
