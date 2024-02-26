from django.conf import settings
from django.contrib.admin import display
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
    from_email = models.EmailField(
        blank=False,
        db_column="from_email",
        default=settings.DEFAULT_FROM_EMAIL,
        help_text=_(
            "From address of e-mail message(s) sent using the template."
        ),
        null=False,
        validators=(EmailValidator(),),
        verbose_name=_("Sender E-mail Address")
    )
    from_name = models.CharField(
        blank=True,
        db_column="from_name",
        max_length=32,
        null=True,
        help_text=_("From name of e-mail message(s) sent using the template."),
        validators=(
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32)
        ),
        verbose_name=_("From Name")
    )
    reply_to_email = models.EmailField(
        blank=False,
        db_column="reply_to_email",
        default=settings.DEFAULT_FROM_EMAIL,
        help_text=_(
            "Reply-To e-mail address of message(s) sent using the template."
        ),
        null=False,
        validators=(EmailValidator(),),
        verbose_name=_("Reply-To E-mail Address")
    )
    reply_to_name = models.CharField(
        blank=True,
        db_column="reply_to_name",
        max_length=32,
        null=True,
        help_text=_(
            "Reply-To e-mail name of message(s) sent using the template."
        ),
        validators=(
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32)
        ),
        verbose_name=_("Reply-To Name")
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

    @property
    @display(description="From Address", ordering="from_email")
    def from_address(self):
        return "%s <%s>" % (self.from_name, self.from_email)

    @property
    @display(description="Reply-To Address", ordering="reply_to_email")
    def reply_to_address(self):
        return "%s <%s>" % (self.reply_to_name, self.reply_to_email)
