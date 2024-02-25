from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.timezone import now
from django.utils.translation import ngettext

from ..models.widget import Widget

from apps.mailer.models.message import MailerMessage


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    """Widget administration."""
    model = Widget
    change_list_template = "widgets_changelist.html"
    date_hierarchy = "created_at"
    fieldsets = (
        ("Widget", {"fields": ("name", "description", "active")}),
        ("Notifications", {"fields": ("email", "template",)}),
        ("Created", {
            "fields": ("created_at", "created_by"),
            "classes": ("collapse",),
        }),
        ("Updated", {
            "fields": ("updated_at", "updated_by"),
            "classes": ("collapse",),
        }),
    )
    list_display = ("name", "active", "email", "template",)
    list_filter = (
        "active",
        ("template", admin.RelatedOnlyFieldListFilter),
        ("created_by", admin.RelatedOnlyFieldListFilter),
        ("updated_by", admin.RelatedOnlyFieldListFilter)
    )
    readonly_fields = ("created_at", "created_by", "updated_at", "updated_by")
    save_as = True
    save_on_top = True
    search_fields = ("name", "description", "email", "created_by", "updated_by")
    show_facets = admin.ShowFacets.ALWAYS
    show_full_result_count = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    def get_urls(self):
        return [
            path("activate/", self.activate_all),
            path("deactivate/", self.deactivate_all),
            path("queueall/", self.queue_all),
        ] + super().get_urls()

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

    def queue_all(self, request):
        self.queue_mail(request, self.model.objects.filter(active=True))
        return HttpResponseRedirect("..")

    @admin.action(
        description=f"Activate selected {model._meta.verbose_name_plural}"
    )
    def activate(self, request, queryset):
        activated = queryset.update(active=True)
        self.message_user(
            request=request,
            message=ngettext(
                singular=(
                    f"%d {self.model._meta.verbose_name} was activated."
                ),
                plural=(
                    f"%d {self.model._meta.verbose_name_plural} were activated."
                ),
                number=activated,
            )
            % activated,
            level=messages.SUCCESS,
        )

    @admin.action(
        description=f"Deactivate selected {model._meta.verbose_name_plural}"
    )
    def deactivate(self, request, queryset):
        deactivated = queryset.update(active=False)
        self.message_user(
            request=request,
            message=ngettext(
                singular=(
                    "%d {self.model._meta.verbose_name}"
                    " was successfully deactivated."
                ),
                plural=(
                    f"%d {self.model._meta.verbose_name_plural}"
                    " were successfully deactivated."
                ),
                number=deactivated,
            )
            % deactivated,
            level=messages.WARNING,
        )

    @admin.action(
        description=(
            f"Queue e-mail for selected {model._meta.verbose_name_plural}"
        )
    )
    def queue_mail(self, request, queryset):
        num_queued = 0
        for obj in queryset:
            if obj.active and obj.email and obj.template:
                if obj.template.active:
                    queue_msg = MailerMessage.objects.create()
                    queue_msg.prepare(widget=obj)
                    queue_msg.save()
                    num_queued += 1

        level = messages.WARNING
        if num_queued >= 1:
            level = messages.SUCCESS
        self.message_user(
            request=request,
            message=ngettext(
                singular=(
                    f"%d {self.model._meta.verbose_name} e-mail"
                    " was queued."
                ),
                plural=(
                    f"%d {self.model._meta.verbose_name_plural} e-mails"
                    " were queued."
                ),
                number=num_queued,
            )
            % num_queued,
            level=level,
        )

    actions = (activate, deactivate, queue_mail,)

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
