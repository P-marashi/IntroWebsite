from django.contrib.auth import get_user_model
from django.contrib.auth import models as AuthModels
from django.db import models
from django.db.models import Q
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _

from intro.core.models import BaseModel


class UserManager(AuthModels.BaseUserManager):
    """ Custom User Manager extends BaseUserManager """
    def _create_user(self, email=None, phone_number=None,
                     password=None, **extra_fields):
        """ Main and private function for storing
            user information on database
        """
        if email:
            email = self.normalize_email(email)
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

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        try:
            user = get_user_model().objects.get(Q(email=email) |
                                                Q(phone_number=phone_number),
                                                is_active=False)
        except get_user_model().DoesNotExist:
            user = None

        if user:
            return user

        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_admin", False)
        return self._create_user(email=email, phone_number=phone_number,
                                 password=password, **extra_fields)

    def create_admin(self, email=None, phone_number=None,
                     password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_admin", True)
        return self._create_user(email=email, phone_number=phone_number,
                                 password=password, **extra_fields)

    def create_superuser(self, email=None, phone_number=None,
                         password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        return self._create_user(email=email, phone_number=phone_number,
                                 password=password, **extra_fields)


# Create your models here.
class User(BaseModel, AuthModels.AbstractBaseUser, AuthModels.PermissionsMixin):
    """ Custom Django User Model
        that extends of AbstractBaseUser
    """
    REGISTRATION_TYPE = (
        ('E', _('Email')),
        ('P', _('Phone')),
    )
    profile_photo = models.ImageField(_("profile photo"), upload_to="users/images/",
                                      null=True, blank=True)
    first_name = models.CharField(_("first name"), max_length=100, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, null=True, blank=True)
    phone_number = models.CharField(_("phone number"), max_length=11,
                                    unique=True, null=True, blank=True, db_index=1)
    email = models.EmailField(_("email"), validators=[EmailValidator],
                              unique=True, null=True, blank=True, db_index=1)
    registration_type = models.CharField(_("registration type"),
                                         choices=REGISTRATION_TYPE,
                                         max_length=2, default="E")
    about = models.CharField(_("about"), max_length=300, null=True, blank=True)
    is_active = models.BooleanField(_("is active"), default=False)
    is_superuser = models.BooleanField(_("is superuser"), default=False)
    is_admin = models.BooleanField(_("is admin"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email or self.phone_number

    @property
    def is_staff(self):
        """ return is_admin value
            when is_staff called
            used for admin panel
        """
        return self.is_admin

    @property
    def full_name(self):
        """ method for getting user fullname
            combine firstname and lastname
        """
        return f"{self.first_name}, {self.last_name}"
