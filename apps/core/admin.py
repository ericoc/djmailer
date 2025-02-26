from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf import settings


admin.site.unregister(Group)
admin.site.site_header = settings.WEBSITE_TITLE
admin.site.site_title = settings.WEBSITE_TITLE
admin.site.index_title = settings.WEBSITE_TITLE
