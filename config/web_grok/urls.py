from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
]
