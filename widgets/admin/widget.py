from django.conf import settings
from django.contrib import admin, messages
from django.utils.timezone import now
from django.utils.translation import ngettext
from django_mail_admin import mail
from django_mail_admin.models import PRIORITY, TemplateVariable, OutgoingEmail

from .comment import WidgetCommentInlineAdmin
from ..models.widget import Widget


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    """Widget administration."""
    model = Widget
    date_hierarchy = "created_at"
    fieldsets = (
        ("Widget", {"fields": ("name", "description", "active")}),
        ("Notifications", {"fields": ("email", "template")}),
        ("Created", {
            "fields": ("created_at", "created_by"),
            "classes": ("collapse",),
        }),
        ("Updated", {
            "fields": ("updated_at", "updated_by"),
            "classes": ("collapse",),
        }),
    )
    inlines = (WidgetCommentInlineAdmin,)
    list_display = ("name", "active", "template")
    list_filter = (
        "active",
        ("template", admin.RelatedOnlyFieldListFilter),
        ("created_by", admin.RelatedOnlyFieldListFilter),
        ("updated_by", admin.RelatedOnlyFieldListFilter)
    )
    search_fields = ("name", "description", "created_by", "updated_by")
    readonly_fields = ("created_at", "created_by", "updated_at", "updated_by")

    @admin.action(
        description=f"Activate selected {model._meta.verbose_name_plural}"
    )
    def activate(self, request, queryset):
        activated = queryset.update(active=True)
        self.message_user(
            request,
            ngettext(
                "%d widget was successfully activated.",
                "%d widgets were successfully activated.",
                activated,
            )
            % activated,
            messages.SUCCESS,
        )

    @admin.action(
        description=f"Deactivate selected {model._meta.verbose_name_plural}"
    )
    def deactivate(self, request, queryset):
        deactivated = queryset.update(active=False)
        self.message_user(
            request,
            ngettext(
                f"%d {self.model._meta.verbose_name} was successfully deactivated.",
                f"%d {self.model._meta.verbose_name_plural} were successfully deactivated.",
                deactivated,
            )
            % deactivated,
            messages.WARNING,
        )

    @admin.action(
        description=(
                f"E-mail status of selected {model._meta.verbose_name_plural}"
        )
    )
    def mail_status(modeladmin, request, queryset):
        sent = 0
        if queryset:
            for obj in queryset:
                if obj and obj.active and obj.email and obj.template:
                    mail.send(
                        sender=settings.ADMINS[0][1],
                        recipients=obj.email,
                        template=obj.template,
                        priority=PRIORITY.now,
                        variable_dict={
                            "NAME": obj.name,
                            "DESCRIPTION": obj.description,
                            "ACTIVE": obj.active,
                            "AUTHOR_NAME": (
                                obj.updated_by.get_short_name() or
                                obj.created_by.get_short_name()
                            ),
                            "AUTHOR_DATE": obj.updated_at or obj.created_at
                        }
                    )
                    sent += 1

        messages.add_message(
            request=request,
            level=messages.SUCCESS,
            message=(
                ngettext(
                    f"%d e-mail has been sent.",
                    f"%d e-mails have been sent.",
                    sent,
                )
                % sent
            )
        )

    actions = (activate, deactivate, mail_status)

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_at = now()
            obj.updated_by = request.user
        if not change:
            obj.created_at = now()
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        if change:
            print(change)
        return super().save_related(request, form, formsets, change)


