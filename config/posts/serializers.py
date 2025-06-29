from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    image = serializers.ImageField(required=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'image', 'caption', 'created_at')
        read_only_fields = ['id', 'user', 'created_at']
