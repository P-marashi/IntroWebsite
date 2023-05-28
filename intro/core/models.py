from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """ Abstract Base Model of Intro project

        Attributes:
        -----------
        created_at: DateTimeField(auto_now_add=True)
        updated_at: DateTimeField(auto_now=True)
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
