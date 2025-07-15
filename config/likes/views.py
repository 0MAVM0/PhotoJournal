from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Like
from posts.models import Post


class LikePostView(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'message': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Post liked.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        like = Like.objects.filter(user=request.user, post_id=post_id).first()
        if not like:
            return Response({'message': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({'message': 'Like removed.'}, status=status.HTTP_200_OK)
