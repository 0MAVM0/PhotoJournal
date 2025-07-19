from rest_framework import serializers
from .models import Chat, Message
from users.models import CustomUser
from users.serializers import UserProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'chat', 'sender', 'sender_username', 'content', 'timestamp')
        read_only_fields = ('id', 'chat', 'sender', 'timestamp', 'sender_username')


class ChatSerializer(serializers.ModelSerializer):
    participants = UserProfileSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('id', 'participants', 'created_at', 'last_message')

    def get_last_message(self, obj):
        last = obj.messages.order_by('-timestamp').first()
        if last:
            return MessageSerializer(last).data
        return None
