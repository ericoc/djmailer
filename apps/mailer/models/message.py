from django.core.validators import (
    EmailValidator, MinLengthValidator, MaxLengthValidator
)
from django.db import models
from django.conf import settings
from django.template import Context, Template
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .status import MailerMessageStatus
from .variable import MailerVariable


class MailerMessage(models.Model):
    """
    Mailer message.
    """
    id = models.AutoField(
        db_column="id",
        editable=False,
        help_text=_("Message identification number."),
        primary_key=True,
        verbose_name=_("Message ID")
    )
    status = models.PositiveIntegerField(
        blank=False,
        choices=MailerMessageStatus.choices,
        db_column="status",
        default=MailerMessageStatus.QUEUED,
        help_text=_("Status of the e-mail message."),
        null=False,
        verbose_name=_("Status")
    )
    from_address = models.EmailField(
        blank=False,
        db_column="from_address",
        default=settings.DEFAULT_FROM_EMAIL,
        help_text=_('Sender ("From") e-mail address of the message.'),
        null=False,
        validators=(EmailValidator(),),
        verbose_name=_("From E-mail Address")
    )
    reply_to_address = models.EmailField(
        blank=False,
        db_column="reply_to_address",
        default=settings.DEFAULT_FROM_EMAIL,
        help_text=_('"Reply-To" e-mail address of the message.'),
        null=False,
        validators=(EmailValidator(),),
        verbose_name=_("Reply-To E-mail Address")
    )
    to_address = models.EmailField(
        blank=False,
        db_column="to_address",
        help_text=_('Primary ("To") recipient e-mail address of the message.'),
        null=False,
        validators=(EmailValidator(),),
        verbose_name=_("Recipient E-mail Address")
    )
    subject = models.CharField(
        blank=False,
        db_column="subject",
        max_length=32,
        null=False,
        help_text=_("Subject of the e-mail message."),
        validators=(
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32)
        ),
        verbose_name=_("E-mail Subject")
    )
    body = models.TextField(
        blank=False,
        db_column="body",
        null=False,
        help_text=_("Body of the e-mail message."),
        verbose_name=_("E-mail Body")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        db_column="created_at",
        editable=False,
        null=False,
        help_text=_("Date and time when the e-mail message was created."),
        verbose_name=_("Created At")
    )
    sent_at = models.DateTimeField(
        blank=False,
        db_column="sent_at",
        default=None,
        editable=False,
        null=True,
        help_text=_("Date and time when the e-mail message was sent."),
        verbose_name=_("Sent At")
    )

    class Meta:
        db_table = "messages"
        default_related_name = "message"
        managed = True
        ordering = ("-id",)
        verbose_name = _("Message")

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.pk
        )

    def __str__(self):
        return "%s <%s> @ %s" % (
            self.subject,
            self.to_address,
            self.created_at.strftime("%c %Z")
        )

    def prepare(self, widget=None):

        if widget and widget.template:
            template = widget.template

            to_address = widget.email
            self.to_address = to_address

            from_address = template.from_address
            self.from_address = from_address

            reply_to_address = template.reply_to_address
            self.reply_to_address = reply_to_address

            context = {
                "WIDGET": widget,
                "TO_ADDRESS": to_address,
                "FROM_ADDRESS": from_address,
                "REPLY_TO_ADDRESS": reply_to_address,
            }
            context = Context(context)
            for i in MailerVariable.objects.all():
                context[i.name] = Template(i.value).render(context=context)
            self.subject = Template(template.subject).render(context=context)
            self.body = Template(template.body).render(context=context)

    @property
    def body_html(self):
        return format_html(self.body)
