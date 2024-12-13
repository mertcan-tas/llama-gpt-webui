from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from app.models import Message, Chat
from app.serializers import MessageSerializer
from app.tasks import chatMessage
from celery.result import AsyncResult
from app.tasks import chatMessage

class ChatMessageAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            with transaction.atomic():
                # Kullanıcı mesajını oluştur
                user_message = serializer.save()

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

class ChatTaskStatusAPIView(APIView):
    """
    Celery görevinin durumunu kontrol eder ve tamamlandıysa AI yanıtını döner.
    """

    def get(self, request, task_id, *args, **kwargs):
        result = AsyncResult(task_id)

        if result.state == "SUCCESS":
            # AI yanıtını güncelle
            response_text = result.result
            ai_message_id = request.query_params.get('ai_message_id')
            try:
                ai_message = Message.objects.get(id=ai_message_id, role='ai')
                ai_message.content = response_text
                ai_message.save()
            except Message.DoesNotExist:
                return Response({"error": "AI message not found."}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "status": result.state,
                "response": response_text
            }, status=status.HTTP_200_OK)

        elif result.state == "PENDING":
            return Response({
                "status": result.state,
                "message": "Task is still being processed."
            }, status=status.HTTP_202_ACCEPTED)

        else:
            return Response({
                "status": result.state,
                "message": "Task failed or unknown error occurred."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
