from django.conf import settings
from django.db import models

from intro.core.models import BaseModel


# Create your models here.
class ImageExamples(BaseModel):
    """ Image model object
        Users can add unlimited
        images to their projects
    """

    image = models.ImageField()

    def __str__(self):
        return self.image


class Features(BaseModel):
    """ Features model object
        Users can add unlimit
        features to their projects
    """
    title = models.TextField()

    def __str__(self):
        return self.text


class Projects(BaseModel):
    """ Project model object
        Users can declare their
        wanted projects by this model
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=5000)
    features = models.ManyToManyField(Features,
                                      related_name="projects", blank=True)
    images = models.ManyToManyField(ImageExamples,
                                    related_name="images", blank=True)
    url_example = models.URLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True,
                             related_name="projects", blank=True)

    def __str__(self):
        return self.title


class Comments(BaseModel):
    """ Comment system for project model """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="all_comments")
    project = models.ForeignKey(Projects,
                                on_delete=models.CASCADE, related_name="comments")
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)

    def __str__(self):
        return self.title
