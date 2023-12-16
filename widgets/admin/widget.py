from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.timezone import now
from django.utils.translation import ngettext

from .comment import WidgetCommentInlineAdmin
from ..models.widget import Widget


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    """Widget administration."""
    model = Widget
    change_list_template = "widgets_changelist.html"
    date_hierarchy = "created_at"
    fieldsets = (
        ("Widget", {"fields": ("name", "description", "active")}),
        ("Notifications", {"fields": ("email",)}),
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
    list_display = ("name", "active",)
    list_filter = (
        "active",
        ("created_by", admin.RelatedOnlyFieldListFilter),
        ("updated_by", admin.RelatedOnlyFieldListFilter)
    )
    search_fields = ("name", "description", "created_by", "updated_by")
    readonly_fields = ("created_at", "created_by", "updated_at", "updated_by")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('activate/', self.activate_all),
            path('deactivate/', self.deactivate_all),
        ]
        return my_urls + urls

    def activate_all(self, request):
        self.model.objects.all().update(active=True)
        self.message_user(request,"All widgets have been activated.")
        return HttpResponseRedirect("..")

    def deactivate_all(self, request):
        self.model.objects.all().update(active=False)
        self.message_user(
            request,
            "All widgets have been deactivated.",
            messages.WARNING
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
                (f"%d {self.model._meta.verbose_name}"
                 " was successfully deactivated."),
                (f"%d {self.model._meta.verbose_name_plural}"
                 " were successfully deactivated."),
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


