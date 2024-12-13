from rest_framework import serializers
from app.models import Message, Chat

class MessageSerializer(serializers.ModelSerializer):
    chat_id = serializers.CharField(write_only=True, required=False) 
    
    class Meta:
        model = Message
        fields = ['id', 'content', 'created_at', 'chat_id']
        read_only_fields = ['id', 'role','created_at']
    
    def create(self, validated_data):
        request_user = self.context['request'].user 
        chat_id = validated_data.pop('chat_id', None)

        if chat_id is None:
            # Yeni bir Chat oluştur
            chat = Chat.objects.create(user=request_user)
        else:
            # Mevcut bir Chat'i bul
            try:
                chat = Chat.objects.get(id=chat_id, user=request_user)
            except Chat.DoesNotExist:
                raise serializers.ValidationError({"chat_id": "Belirtilen sohbet mevcut değil veya size ait değil."})

        # Mesajı oluştur ve chat'e bağla
        message = Message.objects.create(chat=chat, role='user', **validated_data)

        # Eğer chat'in başlığı yoksa, mesajın içeriğini başlık yap
        if not chat.title:
            chat.title = message.content[:50]  # İlk 50 karakter başlık olarak kullanılıyor
            chat.save()

        return message
