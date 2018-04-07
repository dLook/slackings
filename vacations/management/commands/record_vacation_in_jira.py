# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.core.management.base import BaseCommand

from vacations.models import VacationRecord


class Command(BaseCommand):
    def handle(self, *args, **options):
        vacation_records = VacationRecord.objects.filter(
            is_processed=False, date_from=date.today(), sent_to_jira=True)
        for record in vacation_records:
            record.submit_to_jira()
