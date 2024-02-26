from django.contrib.admin import display
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
    from_email = models.EmailField(
        blank=False,
        db_column="from_email",
        default=settings.DEFAULT_FROM_EMAIL,
        help_text=_('Sender ("From") e-mail address of the message.'),
        null=False,
        validators=(EmailValidator(),),
        verbose_name=_("From E-mail Address")
    )
    from_name = models.CharField(
        blank=True,
        db_column="from_name",
        max_length=32,
        null=True,
        help_text=_('Sender name in the e-mail "From" address.'),
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
        help_text=_('"Reply-To" e-mail address of the message.'),
        null=False,
        validators=(EmailValidator(),),
        verbose_name=_("Reply-To E-mail Address")
    )
    reply_to_name = models.CharField(
        blank=True,
        db_column="reply_to_name",
        max_length=32,
        null=True,
        help_text=_('Reply-To name of the message.'),
        validators=(
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32)
        ),
        verbose_name=_("From Name")
    )
    to_email = models.EmailField(
        blank=False,
        db_column="to_email",
        help_text=_('Primary ("To") recipient e-mail address of the message.'),
        null=False,
        validators=(EmailValidator(),),
        verbose_name=_("Recipient E-mail Address")
    )
    to_name = models.CharField(
        blank=True,
        db_column="to_name",
        max_length=32,
        null=True,
        help_text=_('Recipient name in the e-mail "To" address.'),
        validators=(
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32)
        ),
        verbose_name=_("Recipient Name")
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
            self.to_email,
            self.created_at.strftime("%c %Z")
        )

    def prepare(self, widget=None):

        template = widget.template
        self.from_email = template.from_email
        self.from_name = template.from_name
        self.reply_to_email = template.reply_to_email
        self.reply_to_name = template.reply_to_name

        self.to_email = widget.email
        self.to_name = widget.name

        context = Context(
            {
                "WIDGET": widget,

                "TO_ADDRESS": self.to_address,
                "TO_EMAIL": self.to_email,
                "TO_NAME": self.to_name,

                "FROM_ADDRESS": self.from_address,
                "FROM_EMAIL": self.from_email,
                "FROM_NAME": self.from_name,

                "REPLY_TO_ADDRESS": self.reply_to_address,
                "REPLY_TO_EMAIL": self.reply_to_email,
                "REPLY_TO_NAME": self.reply_to_name,
            }
        )
        for item in MailerVariable.objects.all():
            context[item.name] = Template(item.value).render(context=context)

        self.subject = Template(template.subject).render(context=context)
        self.body = Template(template.body).render(context=context)

    @property
    def body_html(self):
        return format_html(self.body)

    @property
    @display(description="From", ordering="from_email")
    def from_address(self):
        return "%s <%s>" % (self.from_name, self.from_email)

    @property
    @display(description="Reply-To", ordering="reply_to_email")
    def reply_to_address(self):
        return "%s <%s>" % (self.reply_to_name, self.reply_to_email)

    @property
    @display(description="To", ordering="to_email")
    def to_address(self):
        return "%s <%s>" % (self.to_name, self.to_email)

    @property
    def cc_addresses(self) -> list:
        cc_addresses = []
        if self.recipient:
            for cc in self.recipient.all():
                if cc.name:
                    cc_addresses.append("%s <%s>" % (cc.name, cc.email))
                else:
                    cc_addresses.append(cc.email)
        return cc_addresses
