from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # Displayed fields in the list view of the admin interface
    list_display = ('title', 'slug', 'category', 'image')

    # Filter options for the list view
    list_filter = ('category',)

    # Fields to enable searching in the admin interface
    search_fields = ('title', 'category__name')