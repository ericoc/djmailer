import logging

from django.db import models
from django.template import Template
from django.utils.translation import gettext_lazy as _

from ..validators import validate_template_syntax

logger = logging.getLogger(__name__)


# TODO: implement cache usage as in post_office
class EmailTemplate(models.Model):
    # TODO: add description about vars available
    class Meta:
        verbose_name = _('Email Template')
        verbose_name_plural = _('Email Templates')

    name = models.CharField(
        verbose_name=_("Template Name"),
        max_length=254
    )

    description = models.TextField(
        verbose_name=_("Template Description"),
        blank=True
    )

    subject = models.CharField(
        verbose_name=_("Subject"),
        max_length=254,
        blank=False,
        validators=[validate_template_syntax]
    )

    email_html_text = models.TextField(
        verbose_name=_("Email HTML Text"),
        blank=True,
        validators=[validate_template_syntax]
    )

    def render_html_text(self, context):
        template = Template(self.email_html_text)
        return template.render(context)

    def render_subject(self, context):
        template = Template(self.subject)
        return template.render(context)

    def __str__(self):
        return self.name


class TemplateVariable(models.Model):
    class Meta:
        verbose_name = _("Template Variable")
        verbose_name_plural = _("Template Variables")

    email = models.ForeignKey(
        to='OutgoingEmail',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        verbose_name=_("Variable Name"),
        max_length=254,
        blank=False
    )

    value = models.TextField(
        verbose_name=_("Variable Value"),
        blank=True
    )

    def __str__(self):
        return self.name
