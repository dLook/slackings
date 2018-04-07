# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .forms import SlackUserExternalAppAdminForm
from .models import SlackUser, ExternalApp, SlackUserExternalApp


class SlackUserAdmin(admin.ModelAdmin):
    list_display = [
        'slack_id', 'name', 'is_online', 'real_name', 'status_text',
        'status_emoji', 'team_id']

admin.site.register(SlackUser, SlackUserAdmin)


class ExternalAppAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

admin.site.register(ExternalApp, ExternalAppAdmin)


class SlackUserExternalAppAdmin(admin.ModelAdmin):
    form = SlackUserExternalAppAdminForm
    raw_id_fields = ['slack_user']
    list_display = ['slack_user', 'app', 'is_active']

admin.site.register(SlackUserExternalApp, SlackUserExternalAppAdmin)
