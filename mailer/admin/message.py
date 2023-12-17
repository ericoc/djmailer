from django.contrib import admin, messages
from django.core.mail import get_connection, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse
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
        ("Addresses", {"fields": ("sender", "recipient",)}),
        ("Contents", {"fields": ("subject", "view_message_field")}),
        ("Time", {"fields": ("created_at", "sent_at",)})
    )
    list_display = ("id", "status", "created_at", "sent_at",)
    list_display_links = ("id", "status",)
    list_filter = ("sender", "status",)
    readonly_fields = (
        "id", "status",
        "sender", "recipient",
        "subject",  "body", "view_message_field",
        "created_at", "sent_at"
    )
    search_fields = (
        "id", "sender", "recipient", "subject", "body", "body_html"
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.GET.get('view') == "true":
            return self.view_message_view(request, object_id)
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.display(description="E-mail Body")
    def view_message_field(self, obj):
        return format_html(
            '<a href="%s" target="_blank">View Message</a>' % (
                reverse(
                    viewname="admin:mailer_mailermessage_change",
                    kwargs={"object_id": obj.pk}
                ) + "?view=true"
            )
        )

    def view_message_view(self, request, obj_id):
        return HttpResponse(
            content=self.get_object(request, obj_id).body_html,
            content_type="text/html"
        )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('cancelall/', self.cancel_all),
            path('sendall/', self.send_all),
        ]
        return my_urls + urls

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def cancel_all(self, request):
        self.cancel_queued_messages(
            request=request,
            queryset=self.model.objects.filter(
                status=MailerMessageStatus.QUEUED
            )
        )
        return HttpResponseRedirect("..")

    def send_all(self, request):
        self.send_queued_messages(
            request=request,
            queryset=self.model.objects.filter(
                status=MailerMessageStatus.QUEUED
            )
        )
        return HttpResponseRedirect("..")

    @admin.action(description="Cancel selected queued Messages")
    def cancel_queued_messages(self, request, queryset):
        level = messages.WARNING
        queued = queryset.filter(status=MailerMessageStatus.QUEUED)
        canceled = len(queued)
        if canceled and canceled > 0:
            queued.update(status=MailerMessageStatus.CANCELED)
            level = messages.SUCCESS

        self.message_user(
            request=request,
            message=ngettext(
                singular="%d queued status e-mail was canceled.",
                plural="%d queued status e-mails were canceled.",
                number=canceled,
            ) % canceled,
            level=level,
        )

    @admin.action(description="Send selected queued Messages")
    def send_queued_messages(self, request, queryset):
        queued = queryset.filter(status=MailerMessageStatus.QUEUED)
        sent = 0
        with get_connection() as connection:
            for obj in queued:
                email_msg = EmailMultiAlternatives(
                    subject=obj.subject,
                    body=obj.body,
                    from_email=obj.sender,
                    reply_to=(obj.sender,),
                    to=(obj.recipient,),
                    headers={
                        "X-Mail-Software": "github.com/ericoc/djadmin",
                        "X-Mail-Software-ID": obj.id,
                        "X-Mail-Software-Item": obj.__repr__(),
                    },
                    connection=connection,
                )
                email_msg.content_subtype = "html"
                if email_msg.send(fail_silently=False):
                    sent += 1

        level = messages.WARNING
        if sent > 0:
            queued.update(status=MailerMessageStatus.SENT, sent_at=now())
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

    actions = (cancel_queued_messages, send_queued_messages,)
