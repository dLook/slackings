# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
import re

from dateutil.parser import parse
import json
import requests

from users.models import SlackUser
from vacations.models import VacationRecord


class VacationHelper(object):
    @staticmethod
    def get_start_end_date(command_text):
        date_strings = re.findall(r'"(?P<dates>[\w .-]+)"', command_text)[:2]

        if len(date_strings) == 2:
            return parse(date_strings[0]), parse(date_strings[1])
        return parse(date_strings[0]), parse(date_strings[0])

    @staticmethod
    def get_comment(command_text):
        match = re.search(r'[C|c]omment: (?P<comment>[\w .,;:?!-_]+)', command_text)
        return match.groupdict().get('comment', '')

    @staticmethod
    def prepare_jira_data(comment, date):
        return {
            'comment': comment,
            'started': '{0}.123+0000'.format(datetime.strftime(date, '%Y-%m-%dT%H:%M:%S')),
            'timeSpent': '7h 30m'  # date should be in Splunk isoformat string format
        }

    @staticmethod
    def submit_for_approval(request):
        payload = request.POST.get('payload')
        if payload:
            request_data = json.loads(payload)
        else:
            request_data = request.POST

        data = {
            "response_type": "in_channel",
            "attachments": [
                {
                    "callback_id": "vacation",
                    "fallback": "Approve vacation!",
                    "title": "Vacation request from user Dino!",
                    "text": "Some random text",
                    "actions": [
                        {
                            "name": "approve",
                            "text": "Approve",
                            "type": "button",
                            "value": "approve"
                        },
                        {
                            "name": "approve2",
                            "text": "Approve",
                            "type": "button",
                            "value": "approve2"
                        },
                    ],
                    "footer": "Vacation will be accepted when 3 or more people approve request!"
                }
            ]
        }
        return data

    @classmethod
    def submit_to_jira(cls, start_date, end_date, comment):
        while start_date <= end_date:
            if start_date.weekday() not in [0, 5, 6]:
                response = requests.post(
                    'https://styria.atlassian.net/rest/api/2/issue/TIP-1/worklog',
                    json=cls.prepare_jira_data(comment=comment, date=start_date),
                    headers={'Authorization': 'Basic ZGluby5sdWtldGljQHN0eXJpYS5ocjo3NDE4NTJkaW5v'})

                if response.status_code != 201:
                    break
            start_date = start_date + timedelta(days=1)

    @classmethod
    def process(cls, data):
        slack_user = SlackUser.objects.get(slack_id=data.get('user_id'))
        command_text = data.get('text')
        comment = cls.get_comment(command_text)
        start_date, end_date = cls.get_start_end_date(command_text)
        vr = VacationRecord(
            slack_user=slack_user,
            date_from=start_date.date(),
            date_to=end_date.date(),
            comment=comment
        )
        vr.save()
        return 'Vacation logged!'
