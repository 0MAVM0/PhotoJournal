from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from posts.models import Post
from .models import Like

class LikePostView(APIView):
    def post(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response({ 'message' : 'Post Was Not Found' }, status=status.HTTP_404_NOT_FOUND)
        
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({ 'message' : 'You Have Already Liked This Post Before' }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({ 'message' : 'Liked' }, status=status.HTTP_201_CREATED)
    
    def delete(self, request, post_id):
        like = Like.objects.filter(user=request.user, post__id=post_id).first()
        if not like:
            return Response({ 'message' : 'You Have Not Liked This Post Yet' }, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({ 'message' : 'Liked Deleted' }, status=status.HTTP_200_OK)
