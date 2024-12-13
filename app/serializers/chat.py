from rest_framework import serializers
from app.models import Chat
from app.serializers import MessageSerializer

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = [ 'id', 'title', 'created_at']

class ChatMessagesSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)  
    
    class Meta:
        model = Chat
        fields = ['id', 'title', 'user', 'messages']
