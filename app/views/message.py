from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from app.serializers import MessageSerializer
from app.models import Message

class MessageCreateAPIView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
