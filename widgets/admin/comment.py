from django.contrib import admin
from django.db import models
from django.forms import Textarea

from ..models.comment import WidgetComment


class WidgetCommentInlineAdmin(admin.TabularInline):
    """Widget Comment inline administration."""
    model = WidgetComment
    extra = 1
    fields = ("text", "created_by", "created_at", "updated_at")
    # fieldsets = (
    #     ("Comment", {"fields": ("text",)}),
    #     ("Author", {
    #         "fields": ("created_by",),
    #         "classes": ("collapse",)
    #     }),
    #     ("Updated", {
    #         "fields": ("updated_at",),
    #         "classes": ("collapse",)
    #     }),
    # )
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 5, "cols": 40})}
    }
    readonly_fields = ("created_by", "created_at", "updated_at")
    user_commented = False

    def has_change_permission(self, request, obj=None):
        if obj and obj.created_by == request.user:
            self.user_commented = True
        return self.user_commented

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def get_extra(self, request, obj=None, **kwargs):
        if self.user_commented:
            return 0
        return 1
