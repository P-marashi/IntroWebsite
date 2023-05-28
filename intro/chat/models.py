from django.conf import settings
from django.db import models

from core.models import BaseModel


# Create your models here.
class Chat(BaseModel):
    support = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name="chats")
    text = models.TextField(max_length=500)
    sender = models.CharField(max_length=500)  # This will be user cookie, that we set on user request

    def __str__(self):
        return "".join(self.text[50])
