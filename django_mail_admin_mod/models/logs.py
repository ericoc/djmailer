from django.db import models
from django.utils.translation import gettext_lazy as _

from ..utils import STATUS
from .outgoing import OutgoingEmail


class Log(models.Model):
    """
    A model to record sending email sending activities.
    """

    STATUS_CHOICES = [
        (STATUS.sent, _("sent")),
        (STATUS.failed, _("failed"))
    ]

    email = models.ForeignKey(
        to=OutgoingEmail,
        editable=False,
        related_name='logs',
        verbose_name=_('Email Address'),
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(
        verbose_name=_('Status'),
        choices=STATUS_CHOICES
    )
    exception_type = models.CharField(
        verbose_name=_('Exception Type'),
        max_length=255,
        blank=True
    )
    message = models.TextField(_('Message'))

    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")

    def __str__(self):
        return str(self.date)
