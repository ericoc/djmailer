from django.contrib import admin

from ..models.variable import MailerVariable


@admin.register(MailerVariable)
class MailerVariableAdmin(admin.ModelAdmin):
    """Variable administration."""
    model = MailerVariable
    fields = list_display = search_fields = ("name", "value")
    save_as = True
    save_on_top = True
    show_facets = admin.ShowFacets.ALWAYS
    show_full_result_count = True
