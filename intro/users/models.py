from django.contrib.auth import models as AuthModels
from django.core.validators import EmailValidator
from django.db import models

from intro.core.models import BaseModel


class UserManager(AuthModels.BaseUserManager):
    """ User Manager """
    def _create_user(self, email=None, phone_number=None,
                     password=None, **extra_fields):
        if email:
            user = self.model(
                email=email,
                **extra_fields
            )

        elif phone_number:
            user = self.model(
                phone_number=phone_number,
                **extra_fields
            )

        else:
            raise ValueError("An Email or Phone number must be given.")

        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone_number=None,
                    password=None, **extra_fields):
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_admin", False)
        return self._create_user(email=email, phone_number=phone_number,
                                 password=password, extra_fields=extra_fields)

    def create_admin(self, email=None, phone_number=None,
                     password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_admin", True)
        return self._create_user(email=email, phone_number=phone_number,
                                 password=password, extra_fields=extra_fields)

    def create_superuser(self, email=None, phone_number=None,
                         password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        return self._create_user(email=email, phone_number=phone_number,
                                 password=password, extra_fields=extra_fields)


# Create your models here.
class User(BaseModel, AuthModels.AbstractBaseUser, AuthModels.PermissionsMixin):
    """ User Model """
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=11,
                                    unique=True, null=True, blank=True)
    email = models.EmailField(validators=[EmailValidator],
                              unique=True, null=True, blank=True)
    about = models.CharField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.full_name

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def full_name(self):
        return f"{self.first_name}, {self.last_name}"
