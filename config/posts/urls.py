from django.urls import path, include
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, MyPostsView, LikedPostsView

urlpatterns = [
    # Posts
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('my/', MyPostsView.as_view(), name='my-posts'),
    path('liked/', LikedPostsView.as_view(), name='liked-posts'),
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),

    # Comments
    path('<int:id>/comments/', include('comments.urls'), name='comment-list-create'),

    # Likes
    path('<int:id>/like/', include('likes.urls'), name='like-post')
]
