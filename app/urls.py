from django.urls import path
from app.views import UserChatListAPIView, ChatDetailAPIView, ChatDeleteAPIView, ChatMessageAPIView, TaskStatusAPIView

urlpatterns = [
    path('user-chats/', UserChatListAPIView.as_view(), name='user-chats'),
    path('chat-messages/<str:id>/', ChatDetailAPIView.as_view(), name='chat-detail'),
    path('chat/<str:id>/delete/', ChatDeleteAPIView.as_view(), name='chat-delete'),
    path('message/', ChatMessageAPIView.as_view(), name='chat-message'),
    path('chat/task_status/', TaskStatusAPIView.as_view(), name='task-status'),
]

