from django.urls import path, include
from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
    MyPostsView,
    LikedPostsView
)

urlpatterns = [
    # Posts
    path('', PostListCreateView.as_view(), name='api-post-list-create'),
    path('my/', MyPostsView.as_view(), name='api-my-posts'),
    path('liked/', LikedPostsView.as_view(), name='api-liked-posts'),
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='api-post-detail'),

    # Comments
    path('<int:post_id>/comments/', include('comments.urls'), name='api-post-comments'),

    # Likes
    path('<int:post_id>/like/', include('likes.urls'), name='api-post-like'),
]
