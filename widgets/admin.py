from django.contrib import admin
from django.utils.timezone import now

from .models import Widget


# Register custom widget model admin.
@admin.register(Widget)
class WidgetsAdmin(admin.ModelAdmin):
    """
    Widget administration.
    """
    model = Widget
    date_hierarchy = "created_at"
    fieldsets = (
        ("Widget", {"fields": ("id", "name", "description", "active")}),
        ("Created", {"fields": ("created_at", "created_by")}),
        ("Updated", {"fields": ("updated_at", "updated_by")}),
    )
    filter_horizontal = ()
    list_display = ("name", "active", "created_by")
    list_filter = (
        "active",
        ("created_by", admin.RelatedOnlyFieldListFilter),
        ("updated_by", admin.RelatedOnlyFieldListFilter)
    )
    search_fields = ("name", "description", "created_by", "updated_by")
    readonly_fields = (
        "id", "created_at", "created_by", "updated_at", "updated_by"
    )

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_at = now()
            obj.updated_by = request.user
        if not change:
            obj.created_at = now()
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
