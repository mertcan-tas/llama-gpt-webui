from shortuuid.django_fields import ShortUUIDField
from django.db import models

from app.models import Chat

class Message(models.Model):
    id = ShortUUIDField(length=16,max_length=40,alphabet="abcdefg1234",primary_key=True,editable=False)
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]
    
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role.capitalize()} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"