from django.contrib import admin, messages
from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html
from django.utils.timezone import now
from django.utils.translation import ngettext

from ..models.message import MailerMessage, MailerMessageStatus


@admin.register(MailerMessage)
class MailerMessageAdmin(admin.ModelAdmin):
    """Message administration."""
    model = MailerMessage
    change_list_template = "message_changelist.html"
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("id",)}),
        ("Contents", {"fields": ("recipient", "subject", "body_html",)}),
        ("Time", {"fields": ("created_at", "sent_at",)})
    )
    list_display = ("id", "status", "created_at", "sent_at", "recipient",)
    list_display_links = ("id", "status",)
    list_filter = ("status",)
    readonly_fields = (
        "id", "status", "recipient", "subject", "body", "created_at", "sent_at",
        "body_html"
    )
    search_fields = ("id", "recipient", "subject", "body",)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('sendall/', self.send_all),
        ]
        return my_urls + urls

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status == MailerMessageStatus.SENT:
            return False
        return super().has_delete_permission(request, obj)

    def send_all(self, request):
        self.send_queued_messages(
            request=request,
            queryset=self.model.objects.filter(
                status=MailerMessageStatus.QUEUED
            )
        )
        return HttpResponseRedirect("..")

    @admin.display(description="E-mail Body")
    def body_html(self, obj):
        return format_html(obj.body)

    @admin.action(description="Send selected Messages")
    def send_queued_messages(self, request, queryset):
        queued = queryset.filter(status=MailerMessageStatus.QUEUED)
        email_msgs = ()
        sent = 0
        for obj in queued:
            email_msg = EmailMultiAlternatives(
                subject=obj.subject,
                body=obj.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=(obj.recipient,),
                headers={
                    "Reply-to": "djadmin@gaw.sh",
                    "X-Mailer": "git@github.com:ericoc/djadmin.git",
                },
            )
            email_msg.content_subtype = "html"
            email_msgs = email_msgs + (email_msg,)

        if email_msgs:
            sent = len(email_msgs)
        with get_connection() as connection:
            connection.send_messages(email_msgs)

        level = messages.WARNING
        if email_msgs and len(email_msgs) > 0:
            queued.update(status=0, sent_at=now())
            level = messages.SUCCESS

        self.message_user(
            request=request,
            message=ngettext(
                singular=f"%d queued status e-mail was sent.",
                plural=f"%d queued status e-mails were sent.",
                number=sent,
            ) % sent,
            level=level,
        )

    actions = (send_queued_messages,)
