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
    change_form_template = "message_changeform.html"
    change_list_template = "message_changelist.html"
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("status",)}),
        ("Addresses", {"fields": ("sender", "recipient",)}),
        ("Contents", {"fields": ("subject", "view_message_field")}),
        ("Time", {"fields": ("created_at", "sent_at",)})
    )
    list_display = ("status", "created_at", "sent_at", "view_message_field")
    list_display_links = ("status", "created_at", "sent_at",)
    list_filter = ("sender", "status",)
    readonly_fields = (
        "status",
        "sender", "recipient",
        "subject", "body", "view_message_field",
        "created_at", "sent_at"
    )
    search_fields = (
        "sender", "recipient", "subject", "body", "body_html"
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.GET.get('view') == "true":
            return self.view_message_view(request, object_id)
        return super().change_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        return [
            path("<int:obj_id>/change/cancel/", self.cancel_queued_message),
            path("<int:obj_id>/change/send/", self.send_queued_message),
            path("cancelall/", self.cancel_all),
            path("sendall/", self.send_all),
        ] + super().get_urls()

    def cancel_queued_message(self, request, obj_id):
        self.cancel_queued_messages(
            request=request,
            queryset=self.model.objects.filter(
                id=obj_id,
                status=MailerMessageStatus.QUEUED
            )
        )
        return HttpResponseRedirect("..")

    def send_queued_message(self, request, obj_id):
        self.send_queued_messages(
            request=request,
            queryset=self.model.objects.filter(
                id=obj_id,
                status=MailerMessageStatus.QUEUED
            )
        )
        return HttpResponseRedirect("..")

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
        obj = self.get_object(request, obj_id)
        content = (
            f"<pre>\nFrom: {obj.sender}\nTo: {obj.recipient}\n"
            f"Subject: {obj.subject}\n</pre><hr>{obj.body_html}\n"
        )
        return HttpResponse(content=content, content_type="text/html")

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
        canceled = 0
        queued = queryset.filter(status=MailerMessageStatus.QUEUED)
        canceled = queued.update(status=MailerMessageStatus.CANCELED)

        level = messages.WARNING
        if canceled > 0:
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
        sent = 0
        queued = queryset.filter(status=MailerMessageStatus.QUEUED)

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
                    obj.sent_at = now()
                    obj.status = MailerMessageStatus.SENT
                    obj.save()
                    sent += 1

        level = messages.WARNING
        if sent > 0:
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
