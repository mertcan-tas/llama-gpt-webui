from django.urls import path
from app.views import MessageCreateAPIView, UserChatListAPIView, ChatDetailAPIView, ChatDeleteAPIView

urlpatterns = [
    path('message-create/', MessageCreateAPIView.as_view(), name='message-create'),
    path('user-chats/', UserChatListAPIView.as_view(), name='user-chats'),
    path('chat-messages/<str:id>/', ChatDetailAPIView.as_view(), name='chat-detail'),
    path('chat/<str:id>/delete/', ChatDeleteAPIView.as_view(), name='chat-delete'),
]

