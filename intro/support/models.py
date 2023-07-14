from django.db import models
from django.utils.translation import gettext_lazy as _

from django_prometheus.models import ExportModelOperationsMixin
from django.conf import settings

from intro.core.models import BaseModel


class Ticket(ExportModelOperationsMixin('Ticket'), BaseModel):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
    )
    parent = models.ForeignKey('self', verbose_name=_("parent"), related_name="replieds",
                               on_delete=models.CASCADE, blank=True,
                               default=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_("user"), on_delete=models.CASCADE)  # ForeignKey to the User model
    title = models.CharField(_("title"), max_length=200)
    file = models.FileField(_("file"), blank=True)
    image = models.ImageField(_("image"), blank=True)
    description = models.TextField(_("descriprion"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def __str__(self):
        return f"{self.title} - {self.user}"
