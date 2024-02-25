from django.contrib.admin import TabularInline

from ...models.recipient import MailerRecipient
from ...models.status import MailerMessageStatus


class MailerRecipientTabularInline(TabularInline):
    model = MailerRecipient
    extra = 1

    def has_add_permission(self, request, obj):
        if obj and obj.status == MailerMessageStatus.QUEUED:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if obj and obj.status == MailerMessageStatus.QUEUED:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status == MailerMessageStatus.QUEUED:
            return True
        return False
