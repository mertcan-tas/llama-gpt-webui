from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.generics import RetrieveAPIView,ListAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from app.serializers import ChatSerializer, ChatMessagesSerializer
from app.permissions import IsOwner
from app.models import Chat

@method_decorator(cache_page(60 * 5), name='dispatch') 
class UserChatListAPIView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Chat.objects.filter(user=self.request.user).order_by('-created_at')
        return queryset

@method_decorator(cache_page(60 * 5), name='dispatch') 
class ChatDetailAPIView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatMessagesSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'

class ChatDeleteAPIView(DestroyAPIView):
    queryset = Chat.objects.all()  
    permission_classes = [IsAuthenticated, IsOwner]  
    lookup_field = 'id'