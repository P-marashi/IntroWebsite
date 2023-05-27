from django.db import models

from intro.core.models import BaseModel


# Create your models here.
class ImageExamples(BaseModel):
    image = models.ImageField()


class Features(BaseModel):
    text = models.TextField()


class Projects(BaseModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=5000)
    features = models.ManyToManyField(Features)
    images = models.ManyToManyField(ImageExamples)
    url_example = models.URLField()
