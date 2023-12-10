import logging

from django.conf import settings
from django.contrib import admin
from django.forms.widgets import TextInput
from django.http import HttpResponse
from django.shortcuts import reverse
from django.template import Context
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import (
    TemplateVariable, OutgoingEmail, EmailTemplate, STATUS, Log,
    Attachment
)
from .fields import CommaSeparatedEmailField
from .forms import OutgoingEmailAdminForm

logger = logging.getLogger(__name__)


# Admin row actions
if 'django_admin_row_actions' in settings.INSTALLED_APPS:
    try:
        from django_admin_row_actions import AdminRowActionsMixin
    except ImportError:
        admin_row_actions = False
    else:
        admin_row_actions = True
else:
    admin_row_actions = False


def get_parent():
    """
    Optionally adds AdminRowActionsMixin to admin.ModelAdmin if django_admin_row_actions is installed
    :return: class to inherit from
    """
    if admin_row_actions:
        class BaseAdmin(AdminRowActionsMixin, admin.ModelAdmin):
            pass
    else:
        class BaseAdmin(admin.ModelAdmin):
            pass

    return BaseAdmin


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'subject')
    readonly_fields = ['preview_template_field']

    def preview_template_field(self, o):
        if o.id:
            url = reverse('admin:mailmod_emailtemplate_change', kwargs={'object_id': o.pk})
            url = url + '?preview_template=true'
            return mark_safe(f'<a href="{url}" target="_blank">Preview this template</a>')
        else:
            return '---'
    preview_template_field.short_description='Preview'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.GET.get('preview_template', '').lower()=='true':
            return self.preview_template_view(request, object_id)
        return super().change_view(request, object_id, form_url, extra_context)

    def preview_template_view(self, request, object_id):
        obj = self.get_object(request, object_id)
        content = obj.render_html_text(Context())
        return HttpResponse(content, content_type='text/html')


class TemplateVariableInline(admin.TabularInline):
    model = TemplateVariable
    extra = 1


def get_message_preview(instance):
    return ('{0}...'.format(instance.message[:25]) if len(instance.message) > 25
            else instance.message)


get_message_preview.short_description = _('Message')


class AttachmentInline(admin.TabularInline):
    model = Attachment.emails.through
    extra = 1
    verbose_name = _("Attachment")
    verbose_name_plural = _("Attachments")


class CommaSeparatedEmailWidget(TextInput):
    def __init__(self, *args, **kwargs):
        super(CommaSeparatedEmailWidget, self).__init__(*args, **kwargs)
        self.attrs.update({'class': 'vTextField'})

    def format_value(self, value):
        # If the value is a string wrap it in a list so it does not get sliced.
        if not value:
            return ''
        if isinstance(value, str):
            value = [value, ]
        return ', '.join([item for item in value])


def requeue(modeladmin, request, queryset):
    """An admin action to requeue emails."""
    queryset.update(status=STATUS.queued)


requeue.short_description = _('Requeue selected emails')


class LogInline(admin.TabularInline):
    model = Log
    can_delete = False

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('date')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class OutgoingEmailAdmin(admin.ModelAdmin):
    inlines = (TemplateVariableInline, AttachmentInline, LogInline)
    list_display = [
        'id', 'to_display', 'subject', 'template', 'from_email', 'status',
        'scheduled_time', 'priority'
    ]
    formfield_overrides = {
        CommaSeparatedEmailField: {'widget': CommaSeparatedEmailWidget}
    }
    actions = [requeue]
    form = OutgoingEmailAdminForm

    def to_display(self, instance):
        return ', '.join(instance.to)

    to_display.short_description = _('To')

    def get_form(self, request, obj=None, **kwargs):
        form = super(OutgoingEmailAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        super(OutgoingEmailAdmin, self).save_model(request, obj, form, change)
        obj.queue()


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')


class LogAdmin(admin.ModelAdmin):
    list_display = ('email', 'status', 'date', 'message')


if getattr(settings, 'MAILMOD_ENABLED', True):
    admin.site.register(EmailTemplate, EmailTemplateAdmin)
    # Without this attachment inline won't have add/edit buttons
    admin.site.register(Attachment, AttachmentAdmin)
    admin.site.register(OutgoingEmail, OutgoingEmailAdmin)
    admin.site.register(Log, LogAdmin)
