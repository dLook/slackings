# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import ModelForm, PasswordInput

from .models import SlackUserExternalApp


class SlackUserExternalAppAdminForm(ModelForm):
    class Meta:
        model = SlackUserExternalApp
        exclude = []
        widgets = {
            'password': PasswordInput(),
        }


class ConnectExternalAppFrom(ModelForm):
    class Meta:
        model = SlackUserExternalApp
        exclude = ['slack_user', 'app', 'is_active']
        widgets = {
            'password': PasswordInput(),
        }
