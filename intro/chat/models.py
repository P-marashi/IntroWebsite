from django.conf import settings
from django.db import models

from intro.core.models import BaseModel


# Create your models here.
class Chat(BaseModel):
    """ Chat model object """

    support = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True, blank=True, related_name="support_chats")
    text = models.TextField(max_length=500)
    anonymous_sender = models.CharField(max_length=500)  # This will be user cookie, that we set on user request
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,  # if user is authenticated, user object will be store
                               on_delete=models.CASCADE,
                               null=True, blank=True, related_name="chats")

    def __str__(self):
        return "".join(self.text[50])
