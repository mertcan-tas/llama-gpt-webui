from rest_framework import serializers
from app.models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = [ 'id', 'title', 'created_at']