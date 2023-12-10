import logging

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class Outbox(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    email_use_tls = models.BooleanField('EMAIL_USE_TLS', default=True)
    email_use_ssl = models.BooleanField('EMAIL_USE_SSL', default=False)
    email_ssl_keyfile = models.CharField('EMAIL_SSL_KEYFILE', max_length=1024, null=True, blank=True)
    email_ssl_certfile = models.CharField('EMAIL_SSL_CERTFILE', max_length=1024, null=True, blank=True)
    email_host = models.CharField('EMAIL_HOST', max_length=1024)
    email_host_user = models.CharField('EMAIL_HOST_USER', max_length=255, null=True, blank=True)
    email_host_password = models.CharField('EMAIL_HOST_PASSWORD', max_length=255, null=True, blank=True)
    email_port = models.PositiveSmallIntegerField('EMAIL_PORT', default=25)
    email_timeout = models.PositiveSmallIntegerField('EMAIL_TIMEOUT', null=True, blank=True)
    active = models.BooleanField(_('Active'), default=False)

    def save(self, *args, **kwargs):
        # Only one item can be active at a time

        if self.active:
            # select all other active items
            qs = type(self).objects.filter(active=True)
            # except self (if self already exists)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            # and deactivate them
            qs.update(active=False)

        super(Outbox, self).save(*args, **kwargs)

    def clean(self):
        if self.email_use_ssl and self.email_use_tls:
            raise ValidationError(
                _(
                    "EMAIL_USE_TLS/EMAIL_USE_SSL are mutually exclusive,"
                    "so only set one of those settings to True."
                )
            )

    def __str__(self):
        return (
            '%(email_host_user)s@%(email_host)s:%(email_port)s' % {
                'email_host_user': self.email_host_user,
                'email_host': self.email_host,
                'email_port': self.email_port
            }
        )

    class Meta:
        verbose_name = _("Outbox")
        verbose_name_plural = _("Outboxes")
