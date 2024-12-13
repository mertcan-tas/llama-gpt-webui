from shortuuid.django_fields import ShortUUIDField
from django.db import models

from account.models import User

class Chat(models.Model):
    id = ShortUUIDField(length=16,max_length=40,alphabet="abcdefg1234",primary_key=True,editable=False)
    
    title = models.CharField(max_length=155, null=True, blank=True, verbose_name="Chat Title")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.id