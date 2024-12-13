from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import Message, Chat

@receiver(post_save, sender=Message)
def create_message_related_models(sender, instance, created, **kwargs):
    if created:
        Chat.objects.create(user=instance)
