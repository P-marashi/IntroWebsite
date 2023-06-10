from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_prometheus.models import ExportModelOperationsMixin

from intro.core.models import BaseModel


# Create your models here.
class Chat(ExportModelOperationsMixin('Chat'), BaseModel):
    """ Chat model object """

    support = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("support"),
                                on_delete=models.CASCADE, null=True,
                                blank=True, related_name="support_chats")
    text = models.TextField(_("text"), max_length=500)

    # This will be user cookie, that we set on user request
    anonymous_sender = models.CharField(_("anonymous user cookie"), max_length=500)

    # if user is authenticated, user object will be store
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_("sender"),
                               on_delete=models.CASCADE,
                               null=True, blank=True, related_name="chats")

    class Meta:
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")

    def __str__(self):
        return "".join(self.text[50])
