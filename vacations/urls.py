# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import VacationRecordView


urlpatterns = [
    url(r'^approve$', VacationRecordView.as_view(), name='approve'),
    url(r'^record$', VacationRecordView.as_view(), name='record'),
]
