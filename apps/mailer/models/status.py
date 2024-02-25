from django.db.models import IntegerChoices


class MailerMessageStatus(IntegerChoices):
    """
    Mailer message status choices.
    """
    SENT = 0
    FAILED = 1
    QUEUED = 2
    CANCELED = 3

    def __repr__(self):
        return "%s: %s (%i)" % (
            self.__class__.__name__,
            self.__str__(),
            self.value
        )

    def __str__(self):
        return self.name
