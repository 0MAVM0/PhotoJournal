from django.urls import path
from .views import HomeView, RegisterPageView, LoginPageView, CreatePostView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterPageView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('create/', CreatePostView.as_view(), name='create-post'),
]
