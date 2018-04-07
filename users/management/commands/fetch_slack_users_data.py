# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import hashlib

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from common.slack_api_endpoints import USERS
from common.mixins import SlackClientMixin

from users.models import SlackUser


class Command(SlackClientMixin, BaseCommand):
    def handle(self, *args, **options):
        response = self.slack_client.api_call(USERS['list'])
        members = response['members']

        for member in members:
            response = self.slack_client.api_call(USERS['detail'], user=member['id'])
            if response['ok']:
                slack_profile = response['profile']
                if slack_profile.get('email'):
                    user, _ = User.objects.get_or_create(
                        email=slack_profile['email'],
                        password=hashlib.sha1(member['id']).hexdigest(),
                        defaults={
                            'username': member['id'],
                            'first_name': member['profile'].get('first_name', ''),
                            'last_name': member['profile'].get('last_name', ''),
                            'is_active': True,
                        }
                    )

                    slack_user, _ = SlackUser.objects.get_or_create(
                        user=user,
                        slack_id=member['id'],
                        team_id=member['team_id'],
                        defaults={
                            'name': member['name'],
                            'real_name': slack_profile['real_name_normalized'],
                            'avatar': slack_profile['image_192'],
                            'status_text': slack_profile.get('status_text', ''),
                            'status_emoji': slack_profile.get('status_emoji', '')
                        }
                    )
