from django.dispatch.dispatcher import Signal

email_queued = Signal()   # sender is OutgoingEmail instance
email_sent = Signal()
email_failed_to_send = Signal()
