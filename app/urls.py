from django.urls import path
from app.views import UserChatListAPIView, ChatDetailAPIView, ChatDeleteAPIView, ChatMessageAPIView, ChatTaskStatusAPIView

urlpatterns = [
    path('user-chats/', UserChatListAPIView.as_view(), name='user-chats'),
    path('chat-messages/<str:id>/', ChatDetailAPIView.as_view(), name='chat-detail'),
    path('chat/<str:id>/delete/', ChatDeleteAPIView.as_view(), name='chat-delete'),

    path('message/', ChatMessageAPIView.as_view(), name='chat-message'),
    path('task-status/<str:task_id>/', ChatTaskStatusAPIView.as_view(), name='chat-task-status'),
]

