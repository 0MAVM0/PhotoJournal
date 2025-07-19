from django.urls import path
from .views import ChatListView, ChatDetailView, StartChatView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-list'),
    path('start/<uuid:user_id>/', StartChatView.as_view(), name='chat-start'),
    path('<int:chat_id>/', ChatDetailView.as_view(), name='chat-detail'),
]
