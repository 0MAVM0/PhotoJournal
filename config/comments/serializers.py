from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'created_at', 'comments_count')
        read_only_fields = ['id', 'user', 'created_at', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()
