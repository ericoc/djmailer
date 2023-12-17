from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
)
from django.core.validators import (
    MinLengthValidator, MaxLengthValidator, EmailValidator
)
from django.db import models


class WidgetGroup(Group):
    pass

    class Meta:
        db_table = "groups"
        db_table_comment = "Groups."
        managed = True
        ordering = ("name",)
        verbose_name = "Group"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    """
    User Manager.
    """

    def create_user(
            self, username=None, email=None, password=None,
            first_name=None, last_name=None,
            is_active=True, is_staff=False, is_superuser=False
    ):
        """
        Create and save user with given username, e-mail address, and password.
        """
        if not username:
            raise ValueError("User name is required.")

        user = self.model(
            username=username, email=email,
            first_name=first_name, last_name=last_name,
            is_active=is_active, is_staff=is_staff, is_superuser=is_superuser
        )
        user.set_unusable_password()
        if password:
            user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self, username=None, email=None, password=None,
            first_name=None, last_name=None,
            is_active=True, is_staff=True, is_superuser=True
    ):
        """
        Create and save user with given email address, username, and password.
        """
        user = self.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name,
            is_active=is_active, is_staff=is_staff, is_superuser=is_superuser
        )
        user.save(using=self._db)
        return user


class WidgetUser(PermissionsMixin, AbstractBaseUser):
    """
    User.
    """
    id = models.AutoField(
        primary_key=True,
        help_text="User identification number.",
        verbose_name="User ID"
    )
    username = models.SlugField(
        blank=False,
        max_length=8,
        help_text="Username for the user account.",
        null=False,
        unique=True,
        validators=[
            MinLengthValidator(limit_value=3),
            MaxLengthValidator(limit_value=16)
        ],
        verbose_name="Username"
    )
    email = models.EmailField(
        default=None,
        max_length=64,
        null=True,
        help_text="E-mail address for the user account.",
        validators=[
            MinLengthValidator(limit_value=5),
            MaxLengthValidator(limit_value=64),
            EmailValidator()
        ],
        verbose_name="E-mail Address"
    )
    first_name = models.CharField(
        default=None,
        max_length=64,
        null=True,
        help_text="First name for the user account.",
        verbose_name="First Name"
    )
    last_name = models.CharField(
        default=None,
        max_length=64,
        null=True,
        help_text="Last name for the user account.",
        verbose_name="Last Name"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the user account was created.",
        verbose_name="Created At"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is the user active?",
        verbose_name="Active?"
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Is the user staff?",
        verbose_name="Staff?"
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text="Is the user a superuser?",
        verbose_name="Superuser?"
    )

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    objects = UserManager()
    last_login = None
    REQUIRED_FIELDS = ("email", "first_name", "last_name")

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.get_username()

    class Meta:
        db_table = "users"
        db_table_comment = "Users."
        default_related_name = "user"
        managed = True
        ordering = ("username",)
        verbose_name = "User"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self):
        return self.get_username()
