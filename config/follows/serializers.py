from rest_framework import serializers
from .models import Follow
from users.serializers import UserProfileSerializer

class FollowSerializer(serializers.ModelSerializer):
    following = UserProfileSerializer(read_only=True)
    following_username = serializers.CharField(source='following.username', read_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'following', 'following_username', 'created_at')
        read_only_fields = ('id', 'created_at', 'following_username')
