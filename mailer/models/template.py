from django.conf import settings
from django.core.validators import (
    EmailValidator, MinLengthValidator, MaxLengthValidator
)
from django.db import models


class MailerTemplate(models.Model):
    """
    Mailer Template.
    """
    id = models.AutoField(
        db_column="id",
        editable=False,
        help_text="Template identification number.",
        primary_key=True,
        verbose_name="Template ID"
    )
    active = models.BooleanField(
        db_column="active",
        default=True,
        help_text="Is the e-mail template active and available?",
        verbose_name="Active?"
    )
    name = models.CharField(
        blank=False,
        db_column="name",
        max_length=32,
        null=False,
        help_text="Name of the e-mail template.",
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32)
        ],
        verbose_name="Template Name"
    )
    description = models.TextField(
        blank=True,
        db_column="description",
        help_text="Description of the e-mail template.",
        verbose_name="Template Description"
    )
    sender = models.EmailField(
        blank=False,
        db_column="sender",
        default=settings.DEFAULT_FROM_EMAIL,
        help_text="From address of e-mail message(s) sent using the template.",
        null=False,
        validators=(EmailValidator(),),
        verbose_name="Sender E-mail Address"
    )
    subject = models.CharField(
        blank=False,
        db_column="subject",
        max_length=32,
        null=False,
        help_text="Subject of e-mail message(s) sent using the template.",
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32)
        ],
        verbose_name="E-mail Subject"
    )
    body = models.TextField(
        blank=False,
        db_column="body",
        help_text="Body of e-mail message(s) sent using the template.",
        null=False,
        verbose_name="E-mail Body"
    )

    class Meta:
        db_table = "templates"
        managed = True
        ordering = ("name",)
        verbose_name = "Template"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self):
        return self.name
