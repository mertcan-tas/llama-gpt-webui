from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from app.models import Message
from app.serializers import MessageSerializer
from app.tasks import chatMessage


class TaskStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Yalnızca giriş yapmış kullanıcılar erişebilir

    def get(self, request, *args, **kwargs):
        task_id = request.query_params.get('task_id')
        
        if not task_id:
            return JsonResponse({"error": "task_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Görev, yalnızca kullanıcının ait olduğu sohbetlere bağlıysa, burada doğrulama yapılabilir
        task_result = AsyncResult(task_id)

        if task_result.ready():  # Eğer işlem tamamlanmışsa
            result = task_result.result
            # Kullanıcının yalnızca kendi sohbetini görmesini sağlamak için:
            ai_message = Message.objects.filter(id=task_result.result['ai_message_id'], chat__user=request.user).first()
            
            if ai_message:
                return JsonResponse({"status": "completed", "result": result}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": "You do not have permission to view this message."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse({"status": "processing"}, status=status.HTTP_200_OK)