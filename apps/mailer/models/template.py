from django.conf import settings
from django.core.validators import (
    EmailValidator, MinLengthValidator, MaxLengthValidator
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class MailerTemplate(models.Model):
    """
    Mailer template.
    """
    id = models.AutoField(
        db_column="id",
        editable=False,
        help_text=_("Template identification number."),
        primary_key=True,
        verbose_name=_("Template ID")
    )
    active = models.BooleanField(
        db_column="active",
        default=True,
        help_text=_("Is the e-mail template active and available?"),
        verbose_name=_("Active?")
    )
    name = models.CharField(
        blank=False,
        db_column="name",
        max_length=32,
        null=False,
        help_text=_("Name of the e-mail template."),
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32)
        ],
        verbose_name=_("Template Name")
    )
    description = models.TextField(
        blank=True,
        db_column="description",
        help_text=_("Description of the e-mail template."),
        verbose_name=_("Template Description")
    )
    from_address = models.EmailField(
        blank=False,
        db_column="from_address",
        default=settings.DEFAULT_FROM_EMAIL,
        help_text=_(
            "From address of e-mail message(s) sent using the template."
        ),
        null=False,
        validators=(EmailValidator(),),
        verbose_name=_("Sender E-mail Address")
    )
    reply_to_address = models.EmailField(
        blank=False,
        db_column="reply_to_address",
        default=settings.DEFAULT_FROM_EMAIL,
        help_text=_(
            "Reply-to address of e-mail message(s) sent using the template."
        ),
        null=False,
        validators=(EmailValidator(),),
        verbose_name=_("Reply-to E-mail Address")
    )
    subject = models.CharField(
        blank=False,
        db_column="subject",
        max_length=32,
        null=False,
        help_text=_("Subject of e-mail message(s) sent using the template."),
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32)
        ],
        verbose_name=_("E-mail Subject")
    )
    body = models.TextField(
        blank=False,
        db_column="body",
        help_text=_("Body of e-mail message(s) sent using the template."),
        null=False,
        verbose_name=_("E-mail Body")
    )

    class Meta:
        db_table = "templates"
        default_related_name = "template"
        managed = True
        ordering = ("name",)
        verbose_name = _("Template")

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self):
        return self.name
