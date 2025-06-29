from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404

from .serializers import CommentSerializer
from posts.models import Post
from .models import Comment


class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [ IsAuthenticatedOrReadOnly ]

    def get_queryset(self):
        post_id = self.kwargs['post_id']

        return Comment.objects.filter(post__id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post=post)


class CommentUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [ IsAuthenticatedOrReadOnly ]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().user:
            raise PermissionDenied('You do not have permission to edit this comment.')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied('You do not have permission to delete this comment.')
        instance.delete()