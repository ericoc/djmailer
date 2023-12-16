from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.timezone import now
from django.utils.translation import ngettext

from ..models.template import MailerTemplate


@admin.register(MailerTemplate)
class MailerTemplateAdmin(admin.ModelAdmin):
    """Widget administration."""
    model = MailerTemplate
    fieldsets = (
        ("Template", {"fields": ("name", "description", "active")}),
        ("Subject", {"fields": ("subject",)}),
        ("Body", {"fields": ("body",)}),
    )
    list_display = ("name", "active",)
    list_filter = ("active",)
    search_fields = ("name", "description", "subject", "body",)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('activate/', self.activate_all),
            path('deactivate/', self.deactivate_all),
        ]
        return my_urls + urls

    def activate_all(self, request):
        self.model.objects.all().update(active=True)
        self.message_user(
            request=request,
            message=(
                f"All {self.model._meta.verbose_name_plural}"
                " have been activated."
            ),
            level=messages.WARNING
        )
        return HttpResponseRedirect("..")

    def deactivate_all(self, request):
        self.model.objects.all().update(active=False)
        self.message_user(
            request=request,
            message=(
                f"All {self.model._meta.verbose_name_plural}"
                " have been deactivated."
            ),
            level=messages.WARNING
        )
        return HttpResponseRedirect("..")

    @admin.action(
        description=f"Activate selected {model._meta.verbose_name_plural}"
    )
    def activate(self, request, queryset):
        activated = queryset.update(active=True)
        self.message_user(
            request,
            ngettext(
                (
                    f"%d {self.model._meta.verbose_name}"
                    " was successfully activated."
                ),
                (
                    f"%d {self.model._meta.verbose_name_plural}"
                    " were successfully activated."
                ),
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
                (
                    "%d {self.model._meta.verbose_name}"
                    " was successfully deactivated."
                ),
                (
                    f"%d {self.model._meta.verbose_name_plural}"
                    " were successfully deactivated."
                ),
                deactivated,
            )
            % deactivated,
            messages.WARNING,
        )

    actions = (activate, deactivate,)

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


