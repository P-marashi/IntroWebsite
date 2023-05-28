from django.db import models
from ..users.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Ticket(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               blank=True, default=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to the User model
    title = models.CharField(max_length=200)
    file = models.FileField(blank=True)
    image = models.ImageField(blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user}"


@receiver(pre_save, sender=Ticket)
def set_ticket_user(sender, instance, **kwargs):
    if not instance.user:
        instance.user = instance.created_by  # Set the user field to the created_by field


class Answer(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=155, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket} - {self.admin}"
