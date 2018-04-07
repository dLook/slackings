# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _

import requests

from users.models import SlackUser


class VacationRecord(models.Model):
    slack_user = models.ForeignKey(
        SlackUser, verbose_name=_('Slack user'), related_name='vacation')
    date_from = models.DateField(_('Date from'))
    date_to = models.DateField(_('Date to'))
    comment = models.CharField(_('Comment'), max_length=255, default='', blank=True)
    sent_to_jira = models.BooleanField(_('Send to JIRA'), default=True)
    is_processed = models.BooleanField(_('Is processed'), default=False)

    def __str__(self):
        return self.slack_user.name

    class Meta:
        verbose_name = _('Vacation record')
        verbose_name_plural = _('Vacation records')
        unique_together = ('slack_user', 'date_from', 'date_to')

    @staticmethod
    def prepare_jira_log_data(comment, date):
        return {
            'comment': comment,
            'started': '{0}.123+0000'.format(datetime.strftime(date, '%Y-%m-%dT%H:%M:%S')),
            'timeSpent': '7h 30m'  # date should be in Splunk isoformat string format
        }

    def submit_to_jira(self):
        start_date = self.date_from
        while start_date <= self.date_to:
            if start_date.weekday() not in [0, 5, 6]:
                response = requests.post(
                    'https://styria.atlassian.net/rest/api/2/issue/TIP-1/worklog',
                    json=self.prepare_jira_log_data(comment=self.comment, date=start_date),
                    headers={
                        'Authorization': ''})

                if response.status_code != 201:
                    break

            start_date = start_date + timedelta(days=1)
