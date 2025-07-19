from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from users.models import CustomUser


class ChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chats = Chat.objects.filter(participants=request.user).prefetch_related('participants', 'messages')
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)


class ChatDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
        messages = chat.messages.order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required.'}, status=400)

        message = Message.objects.create(chat=chat, sender=request.user, content=content)
        return Response(MessageSerializer(message).data, status=201)


class StartChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        other_user = get_object_or_404(CustomUser, id=user_id)
        if other_user == request.user:
            return Response({'error': "You can't start a chat with yourself."}, status=400)

        chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
        if not chat:
            chat = Chat.objects.create()
            chat.participants.set([request.user, other_user])

        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=201)
