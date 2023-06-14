from django.db import models
from django.conf import settings

from intro.users.models import User
from intro.core.models import BaseModel


class Ticket(BaseModel):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
    )
    parent = models.ForeignKey('self', related_name="replieds",
                               on_delete=models.CASCADE, blank=True,
                               null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ForeignKey to the User model
    title = models.CharField(max_length=200)
    file = models.FileField(blank=True)
    image = models.ImageField(blank=True)
    description = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.title} - {self.user} "
