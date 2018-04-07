# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.core.management.base import BaseCommand

from users.models import SlackUser
from vacations.models import VacationRecord


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = date.today()
        start_vacations = VacationRecord.objects.filter(date_from=today)
        for item in start_vacations:
            SlackUser.set_status(
                slack_user_id=item.slack_user.slack_id,
                status_text='Vacationing!',
                status_emoji=':palm_tree:'
            )

        end_vacations = VacationRecord.objects.filter(date_to=today)
        for item in end_vacations:
            SlackUser.set_status(
                slack_user_id=item.slack_user.slack_id,
                status_text='',
                status_emoji=''
            )
