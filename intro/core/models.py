from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class BaseModel(models.Model):
    """ Abstract Base Model of Intro project

        Attributes:
        -----------
        created_at: DateTimeField(auto_now_add=True)
        updated_at: DateTimeField(auto_now=True)
    """

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        abstract = True
