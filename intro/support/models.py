from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from intro.users.models import User
from intro.core.models import BaseModel


class Ticket(BaseModel):
    parent = models.ForeignKey('self', verbose_name=_("parent"), related_name="replieds",
                               on_delete=models.CASCADE, blank=True,
                               default=True, null=True)
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)  # ForeignKey to the User model
    title = models.CharField(_("title"), max_length=200)
    file = models.FileField(_("file"), blank=True)
    image = models.ImageField(_("image"), blank=True)
    description = models.TextField(_("descriprion"))

    def __str__(self):
        return f"{self.title} - {self.user}"


@receiver(pre_save, sender=Ticket)
def set_ticket_user(sender, instance, **kwargs):
    if not instance.user:
        instance.user = instance.created_by  # Set the user field to the created_by field


class Answer(BaseModel):
    STATUS_CHOICES = [
        ('O', 'Open'),
        ('I', 'In Progress'),
        ('S', 'Solved'),
    ]
    ticket = models.ForeignKey(Ticket, verbose_name=_("ticket"), on_delete=models.CASCADE)
    admin = models.ForeignKey(User, verbose_name=_("admin"), on_delete=models.CASCADE)
    response = models.TextField(_("response"))
    status = models.CharField(_("status"), choices=STATUS_CHOICES,
                              max_length=155, default="O")

    def __str__(self):
        return f"{self.ticket} - {self.admin}"
