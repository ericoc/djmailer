from django.core.validators import (
    EmailValidator, MinLengthValidator, MaxLengthValidator
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from .message import MailerMessage


class MailerRecipient(models.Model):
    """
    Mailer recipient.
    """
    id = models.AutoField(
        db_column="id",
        editable=False,
        help_text=_("Recipient identification number."),
        primary_key=True,
        verbose_name=_("Recipient ID")
    )
    email = models.EmailField(
        blank=False,
        db_column="email",
        help_text=_("Recipient address of a message."),
        null=False,
        validators=(EmailValidator(),),
        verbose_name=_("Recipient E-mail Address")
    )
    name = models.CharField(
        blank=True,
        db_column="name",
        default=None,
        max_length=32,
        null=True,
        help_text=_("Recipient Name"),
        validators=(
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32)
        ),
        verbose_name=_("Recipient Name")
    )
    message = models.ForeignKey(
        blank=False,
        db_column="message",
        help_text=_("Message related to the recipient."),
        null=False,
        to=MailerMessage,
        to_field="id",
        on_delete=models.CASCADE,
        verbose_name=_("Message")
    )

    class Meta:
        db_table = "recipients"
        default_related_name = "recipient"
        managed = True
        ordering = ("-id",)
        unique_together = (("email", "message"),)
        verbose_name = _("Recipient")

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self):
        return "%s <%s>" % (self.email, self.name)
