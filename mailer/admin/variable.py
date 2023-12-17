from django.contrib import admin
from ..models.variable import MailerVariable


@admin.register(MailerVariable)
class MailerVariableAdmin(admin.ModelAdmin):
    """Variable administration."""
    model = MailerVariable
    fields = list_display = search_fields = ("name", "value")
