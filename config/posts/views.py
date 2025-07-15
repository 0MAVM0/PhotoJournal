from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from .serializers import PostSerializer
from .models import Post


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.select_related('user').prefetch_related('likes', 'comments').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('user').prefetch_related('likes', 'comments').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        post = self.get_object()
        if post.user != self.request.user:
            raise PermissionDenied('You do not have permission to edit this post.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('You do not have permission to delete this post.')
        instance.delete()


class MyPostsView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).select_related('user').prefetch_related('likes', 'comments').order_by('-created_at')

    def get_serializer_context(self):
        return {'request': self.request}


class LikedPostsView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(likes__user=self.request.user).select_related('user').prefetch_related('likes', 'comments').order_by('-created_at')

    def get_serializer_context(self):
        return {'request': self.request}
