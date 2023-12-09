# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoMailAdminModConfig(AppConfig):
    name = 'django_mail_admin_mod'
    verbose_name = _('Mail Admin Mod')
    default_auto_field = 'django.db.models.AutoField'
