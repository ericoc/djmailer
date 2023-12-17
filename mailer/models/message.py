from django.core.validators import (
    EmailValidator, MinLengthValidator, MaxLengthValidator
)
from django.db import models
from django.template import Context, Template

import settings
from ..models.variable import MailerVariable


class MailerMessageStatus(models.IntegerChoices):
    SENT = 0
    FAILED = 1
    QUEUED = 2
    CANCELED = 3

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__str__()} ({self.value})"

    def __str__(self):
        return self.name


class MailerMessage(models.Model):
    """
    Mailer Message.
    """
    id = models.AutoField(
        db_column="id",
        editable=False,
        help_text="Message identification number.",
        primary_key=True,
        verbose_name="Message ID"
    )
    status = models.PositiveIntegerField(
        blank=False,
        choices=MailerMessageStatus.choices,
        db_column="status",
        default=MailerMessageStatus.QUEUED,
        help_text="Status of the e-mail message.",
        null=False,
        verbose_name="Message Status"
    )
    sender = models.EmailField(
        blank=False,
        db_column="sender",
        default=settings.DEFAULT_FROM_EMAIL,
        help_text="E-mail address of the sender of the e-mail message.",
        null=False,
        validators=(EmailValidator(),),
        verbose_name="Sender E-mail Address"
    )
    recipient = models.EmailField(
        blank=False,
        db_column="recipient",
        help_text="E-mail address of the recipient of the e-mail message.",
        null=False,
        validators=(EmailValidator(),),
        verbose_name="Recipient E-mail Address"
    )
    subject = models.CharField(
        blank=False,
        db_column="subject",
        max_length=32,
        null=False,
        help_text="Subject of the e-mail message.",
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32)
        ],
        verbose_name="E-mail Subject"
    )
    body = models.TextField(
        blank=False,
        db_column="body",
        null=False,
        help_text="Body of the e-mail message.",
        verbose_name="E-mail Body"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        db_column="created_at",
        editable=False,
        null=False,
        help_text="Date and time when the e-mail message was created.",
        verbose_name="Created At"
    )
    sent_at = models.DateTimeField(
        blank=False,
        db_column="sent_at",
        default=None,
        editable=False,
        null=True,
        help_text="Date and time when the e-mail message was sent.",
        verbose_name="Sent At"
    )

    def prepare(self, widget=None):
        if widget:
            template = widget.template
            self.sender = template.sender
            self.recipient = widget.email
            context = {
                "widget": widget,
                "RECIPIENT": widget.email,
                "SENDER": template.sender
            }
            for global_variable in MailerVariable.objects.all():
                context[global_variable.name] = global_variable.value
            context = Context(context)
            self.subject = Template(template.subject).render(context)
            self.body = Template(template.body).render(context)

    class Meta:
        db_table = "messages"
        managed = True
        ordering = ("-sent_at", "-created_at", "-id",)
        verbose_name = "Message"

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__str__()} ({self.pk})"

    def __str__(self):
        return f"<{self.recipient}> / {self.created_at.strftime('%c %Z')}"
