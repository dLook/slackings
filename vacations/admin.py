# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import VacationRecord


class VacationRecordAdmin(admin.ModelAdmin):
    pass

admin.site.register(VacationRecord, VacationRecordAdmin)
