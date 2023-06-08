from django.db import models
from django.utils.text import slugify

from intro.core.models import BaseModel


class Category(BaseModel):
    """ Category model using for post categories """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BlogPost(BaseModel):
    """ Blog post model object """

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # A slug field to create SEO-friendly URLs
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Relationship with the Category model
    image = models.ImageField(upload_to='blog_images/', null=True)  # An image field to store blog post images
    text = models.TextField()  # The main content of the blog post

    def save(self, *args, **kwargs):
        # Auto-generate the slug from the title using the slugify function
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
