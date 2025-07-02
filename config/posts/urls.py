from django.urls import path, include
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, MyPostsView

urlpatterns = [
    # Posts
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('my/', MyPostsView.as_view(), name='my-posts'),
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),

    # Comments
    path('<int:id>/comments/', include('comments.urls')),

    # Likes
    path('<int:id>/like/', include('likes.urls'))
]
