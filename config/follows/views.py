from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Follow
from users.models import CustomUser
from .serializers import FollowSerializer


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response({'message': "You can't follow yourself."}, status=400)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
        if not created:
            return Response({'message': "You already follow this user."}, status=400)

        return Response({'message': "Followed."}, status=201)

    def delete(self, request, user_id):
        follow = Follow.objects.filter(follower=request.user, following__id=user_id).first()
        if not follow:
            return Response({'message': "You don't follow this user."}, status=400)
        follow.delete()
        return Response({'message': "Unfollowed."}, status=200)


class FollowersListView(APIView):
    def get(self, request, user_id):
        followers = Follow.objects.filter(following__id=user_id)
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)


class FollowingListView(APIView):
    def get(self, request, user_id):
        following = Follow.objects.filter(follower__id=user_id)
        serializer = FollowSerializer(following, many=True)
        return Response(serializer.data)
