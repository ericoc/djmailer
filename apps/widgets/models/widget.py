from django.contrib.auth import get_user_model
from django.core.validators import (
    EmailValidator, MinLengthValidator, MaxLengthValidator
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.mailer.models.template import MailerTemplate


class Widget(models.Model):
    """
    Widget.
    """
    id = models.AutoField(
        db_column="id",
        editable=False,
        help_text=_("Widget identification number."),
        primary_key=True,
        verbose_name=_("Widget ID")
    )
    name = models.SlugField(
        blank=False,
        db_column="name",
        max_length=32,
        null=False,
        help_text=_("Name of the widget."),
        validators=[
            MinLengthValidator(limit_value=2),
            MaxLengthValidator(limit_value=32)
        ],
        verbose_name=_("Widget Name")
    )
    description = models.TextField(
        blank=True,
        db_column="description",
        help_text=_("Description of the widget."),
        verbose_name=_("Widget Description")
    )
    active = models.BooleanField(
        db_column="active",
        default=True,
        help_text=_("Is the widget active and available?"),
        verbose_name=_("Active?")
    )
    email = models.EmailField(
        blank=True,
        db_column="email",
        default=None,
        help_text=_("E-mail address for widget notifications."),
        null=True,
        validators=(EmailValidator(),),
        verbose_name=_("E-mail Address")
    )
    template = models.ForeignKey(
        db_column="template",
        default=None,
        help_text=_("E-mail template to be used for for widget notifications."),
        null=True,
        to=MailerTemplate,
        to_field="id",
        on_delete=models.SET_NULL,
        verbose_name=_("E-mail Template")
    )
    created_at = models.DateTimeField(
        blank=False,
        db_column="created_at",
        editable=False,
        null=False,
        auto_now_add=True,
        help_text=_("Date and time when the widget was created."),
        verbose_name=_("Created At")
    )
    created_by = models.ForeignKey(
        blank=False,
        db_column="created_by",
        editable=False,
        null=True,
        help_text=_("User who created the widget."),
        related_name="+",
        to=get_user_model(),
        on_delete=models.SET_NULL,
        verbose_name=_("Created By")
    )
    updated_at = models.DateTimeField(
        blank=False,
        db_column="updated_at",
        editable=False,
        default=None,
        null=True,
        help_text=_("Date and time when the widget was last updated."),
        verbose_name=_("Updated At")
    )
    updated_by = models.ForeignKey(
        blank=False,
        db_column="updated_by",
        editable=False,
        default=None,
        help_text=_("User who last updated the widget."),
        null=True,
        related_name="+",
        to=get_user_model(),
        on_delete=models.SET_NULL,
        verbose_name=_("Updated By")
    )

    class Meta:
        db_table = "widgets"
        managed = True
        ordering = ("name",)
        verbose_name = _("Widget")

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self):
        return self.name
