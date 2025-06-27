from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.core.exceptions import PermissionDenied
from .serializers import PostSerializer
from .models import Post


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        if self.request.user != self.get_object().user:
            raise PermissionDenied('You do not have permission to edit this post.')
        serializer.save()
    
    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied('You do not have permission to delete this post.')
        instance.delete()
