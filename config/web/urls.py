from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterPageView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='delete-post'),
    path('post/<int:pk>/edit/', EditPostView.as_view(), name='edit-post'),
    path('like/<int:post_id>/', ajax_like_post, name='ajax-like-post'),
    path('comment/<int:post_id>/', ajax_comment_post, name='ajax-comment-post'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('liked/', LikedPostsView.as_view(), name='liked-posts'),
    path('users/search/', UserSearchView.as_view(), name='user-search'),
]
