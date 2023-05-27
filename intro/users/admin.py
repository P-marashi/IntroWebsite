from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User


UserAdmin.ordering = (
    ("email", "email")
)
UserAdmin.list_display = (
    ("email", "email")
)
UserAdmin.list_filter = [
    "is_admin"
]


# Register your models here.
admin.site.register(User, UserAdmin)
