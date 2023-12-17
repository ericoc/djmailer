from django.contrib.auth import get_user_model
from django.core.validators import (
    EmailValidator, MinLengthValidator, MaxLengthValidator
)
from django.db import models

from mailer.models.template import MailerTemplate


class Widget(models.Model):
    """
    Widget.
    """
    id = models.AutoField(
        db_column="id",
        editable=False,
        help_text="Widget identification number.",
        primary_key=True,
        verbose_name="Widget ID"
    )
    name = models.SlugField(
        blank=False,
        db_column="name",
        max_length=32,
        null=False,
        help_text="Name of the widget.",
        validators=[
            MinLengthValidator(limit_value=2),
            MaxLengthValidator(limit_value=32)
        ],
        verbose_name="Widget Name"
    )
    description = models.TextField(
        blank=True,
        db_column="description",
        help_text="Description of the widget.",
        verbose_name="Widget Description"
    )
    active = models.BooleanField(
        db_column="active",
        default=True,
        help_text="Is the widget active and available?",
        verbose_name="Active?"
    )
    email = models.EmailField(
        blank=True,
        db_column="email",
        default=None,
        help_text="E-mail address for widget notifications.",
        null=True,
        validators=(EmailValidator(),),
        verbose_name="E-mail Address"
    )
    template = models.ForeignKey(
        db_column="template",
        default=None,
        help_text="E-mail template to be used for for widget notifications.",
        null=True,
        to=MailerTemplate,
        to_field="id",
        on_delete=models.PROTECT,
        verbose_name="E-mail Template"
    )
    created_at = models.DateTimeField(
        blank=False,
        db_column="created_at",
        editable=False,
        null=False,
        auto_now_add=True,
        help_text="Date and time when the widget was created.",
        verbose_name="Created At"
    )
    created_by = models.ForeignKey(
        blank=False,
        db_column="created_by",
        editable=False,
        null=False,
        help_text="User who created the widget.",
        related_name="+",
        to=get_user_model(),
        on_delete=models.PROTECT,
        verbose_name="Created By"
    )
    updated_at = models.DateTimeField(
        blank=False,
        db_column="updated_at",
        editable=False,
        default=None,
        null=True,
        help_text="Date and time when the widget was last updated.",
        verbose_name="Updated At"
    )
    updated_by = models.ForeignKey(
        blank=False,
        db_column="updated_by",
        editable=False,
        default=None,
        help_text="User who last updated the widget.",
        null=True,
        related_name="+",
        to=get_user_model(),
        on_delete=models.PROTECT,
        verbose_name="Updated By"
    )

    class Meta:
        db_table = "widgets"
        managed = True
        ordering = ("-updated_at", "-created_at", "-id",)
        verbose_name = "Widget"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self):
        return self.name
