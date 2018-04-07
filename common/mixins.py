# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings

from slackclient import SlackClient


class SlackClientMixin(object):
    def __init__(self):
        self.slack_client = SlackClient(settings.SLACK_TOKEN)
