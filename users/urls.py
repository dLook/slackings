# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    SlackUserStatusGridView, UserChangeEventListener, ConnectExternalAppFormView,
    ConnectExternalAppSuccessView)

urlpatterns = [
    url(r'^connect/app-(?P<app_id>\d+)/user-(?P<slack_user_id>\d+)$',
        ConnectExternalAppFormView.as_view(), name='connect_external_app_form'),
    url(r'^connect/success',
        ConnectExternalAppSuccessView.as_view(), name='connect_external_app_success'),
    url(r'^status-grid$', SlackUserStatusGridView.as_view(), name='status_grid'),
    url(r'^event-listener$', UserChangeEventListener.as_view(), name='user_change'),
]
