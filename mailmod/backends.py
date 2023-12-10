import logging
import threading

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.smtp import EmailBackend

import settings
from .mail import create
from .models import create_attachments
from .utils import PRIORITY

logger = logging.getLogger(__name__)


class CustomEmailBackend(EmailBackend):
    def __init__(
        self,
        host=settings.EMAIL_HOST or 'localhost',
        port=settings.EMAIL_PORT or 25,
        username=None,
        password=None,
        fail_silently=False,
        **kwargs
    ):
        super(CustomEmailBackend, self).__init__(fail_silently=fail_silently)
        self.host = host or settings.EMAIL_HOST or 'localhost'
        self.port = port or settings.EMAIL_PORT or 25
        self.username = username or None
        self.password = password or None
        self.connection = None
        self._lock = threading.RLock()


class OutboxEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        for msg in email_messages:
            try:
                email = create(
                    sender=msg.from_email,
                    recipients=msg.to,
                    cc=msg.cc,
                    bcc=msg.bcc,
                    subject=msg.subject,
                    message=msg.body,
                    headers=msg.extra_headers,
                    priority=PRIORITY.medium,
                )
                alternatives = getattr(msg, 'alternatives', [])
                for content, mimetype in alternatives:
                    if mimetype == 'text/html':
                        email.html_message = content
                        email.save()

                if msg.attachments:
                    attachments = create_attachments(msg.attachments)
                    email.attachments.add(*attachments)

            except Exception:
                if not self.fail_silently:
                    raise
                logger.exception('Email queue failed')

        return len(email_messages)
