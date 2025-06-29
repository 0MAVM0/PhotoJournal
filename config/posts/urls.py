from django.urls import path, include
from .views import PostListCreateView, PostRetrieveUpdateDestroyView

urlpatterns = [
    # Posts
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),

    # Comments
    path('<int:id>/comments/', include('comments.urls')),

    # Likes
]
