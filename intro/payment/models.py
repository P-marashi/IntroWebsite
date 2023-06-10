from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from intro.core.models import BaseModel


# Create your models here.
class Transaction(BaseModel):
    TRANSACTION_STATUS = (
        ("S", _("Success")),
        ("F", _("Failed")),
        ("P", _("Pending")),
        ("N", _("Not Paid")),
    )
    title = models.CharField(_("Title"), max_length=50)
    amount = models.IntegerField(_("amount"))
    description = models.TextField(_("description"), max_length=500, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"),
                             on_delete=models.CASCADE, related_name="transactions")
    authority = models.TextField(_("authority"), max_length=500, null=True, blank=True)
    refID = models.TextField(_("refrence id"), max_length=500, null=True, blank=True)
    status = models.CharField(choices=TRANSACTION_STATUS, default="N")

    def __str__(self):
        return self.title
