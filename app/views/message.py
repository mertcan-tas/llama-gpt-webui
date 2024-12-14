from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from app.models import Message
from app.serializers import MessageSerializer
from app.tasks import chatMessage
from rest_framework.permissions import IsAuthenticated

class ChatMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            with transaction.atomic():
                # Kullanıcı mesajını oluştur
                user_message = serializer.save()

                # Yalnızca kullanıcının ait olduğu sohbeti doğrula
                if user_message.chat.user != request.user:
                    return Response({"error": "You do not have permission to send a message in this chat."}, status=status.HTTP_403_FORBIDDEN)

                # AI mesajı oluşturmak için Celery görevi başlat
                task = chatMessage.delay(user_message.content)

                # AI yanıtını geçici olarak sisteme ekleyin (Celery yanıt beklerken)
                ai_message = Message.objects.create(
                    chat=user_message.chat, role='ai', content="", created_at=None
                )

                return Response({
                    "task_id": task.id,
                    "message": "Your message has been sent to the AI for processing.",
                    "chat_id": user_message.chat.id,
                    "user_message": user_message.content,
                    "ai_message_id": ai_message.id
                }, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)