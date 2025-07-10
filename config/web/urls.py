from django.urls import path
from .views import HomeView, RegisterPageView, LoginPageView, CreatePostView, DeletePostView, EditPostView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterPageView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='delete-post'),
    path('post/<int:pk>/edit/', EditPostView.as_view(), name='edit-post'),
]
