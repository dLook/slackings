# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from users.models import SlackUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        qs = SlackUser.objects.filter(id=17)
        SlackUser.get_user_presence(qs)
