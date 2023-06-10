from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from intro.core.models import BaseModel
from intro.payment.models import Transaction


# Create your models here.
class ImageExamples(BaseModel):
    """ Image model object
        Users can add unlimited
        images to their projects
    """

    image = models.ImageField(_("image"), upload_to="project/images")

    def __str__(self):
        return self.image


class Features(BaseModel):
    """ Features model object
        Users can add unlimit
        features to their projects
    """

    title = models.TextField(_("title"), max_length=100)

    def __str__(self):
        return self.title


class Projects(BaseModel):
    """ Project model object
        Users can declare their
        wanted projects by this model
    """
    title = models.CharField(_("title"), max_length=100)
    slug = models.SlugField(_("slug"), max_length=50, unique=True)
    description = models.TextField(_("description"), max_length=5000)
    features = models.ManyToManyField(Features, verbose_name=_("features"),
                                      related_name="projects", blank=True)
    images = models.ManyToManyField(ImageExamples, verbose_name=_("images"),
                                    related_name="images", blank=True)
    url_example = models.URLField(_("example url"), null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"),
                             on_delete=models.SET_NULL, null=True,
                             related_name="projects", blank=True)
    amount = models.IntegerField(_("amount"), null=True, blank=True)
    transaction = models.ManyToManyField(Transaction, blank=True,
                                         verbose_name=_("transaction"))

    def __str__(self):
        return self.title


class Comments(BaseModel):
    """ Comment system for project model """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"),
                             on_delete=models.CASCADE, related_name="all_comments")
    project = models.ForeignKey(Projects, verbose_name=_("project"),
                                on_delete=models.CASCADE, related_name="comments")
    title = models.CharField(_("title"), max_length=100)
    text = models.TextField(_("text"), max_length=500)

    def __str__(self):
        return self.title
