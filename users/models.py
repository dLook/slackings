# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from common.mixins import SlackClientMixin
from common.slack_api_endpoints import USERS
from .settings import EMOJI_MAPPING


class SlackUser(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, verbose_name=_("User"), related_name='slack_user')
    slack_id = models.CharField(_("Slack ID"), max_length=20, unique=True)
    team_id = models.CharField(_("Slack team ID"), max_length=20)
    name = models.CharField(_("Slack name"), max_length=100)
    real_name = models.CharField(_("Slack real name"), max_length=100)
    avatar = models.URLField(_("Slack avatar"), max_length=255, blank=True, default='')
    status_text = models.CharField(_("Slack status text"), max_length=255, blank=True, default='')
    status_emoji = models.CharField(_("Slack status emoji"), max_length=100, blank=True, default='')
    is_online = models.BooleanField(_('Is online'), default=False)
    last_modified = models.DateTimeField(_("Last modified"), auto_now=True)

    class Meta:
        verbose_name = _("Slack user")
        verbose_name_plural = _("Slack users")
        unique_together = ('slack_id', 'team_id')
        ordering = ("-last_modified",)

    def __str__(self):
        return self.name

    @staticmethod
    def extract_data_from_slack(data):
        """
        Extracts data from Slack `user.list` response.
        :param data: object, JSON response with formated values.
        :return: dict, Dictionary of structured values.
        """
        return {
            'slack_id': data.get('id'),
            'team_id': data.get('team_id'),
            'name': data.get('name'),
            'avatar': data['profile'].get('image_192'),
            'real_name': data['profile'].get('real_name_normalized', ''),
            'status_text': data['profile'].get('status_text', ''),
            'status_emoji': data['profile'].get('status_emoji', ''),
        }

    @classmethod
    def get_all_with_set_status(cls):
        return cls.objects.exclude(Q(status_emoji='') | Q(status_text=''))

    @classmethod
    def get_all_with_important_statuses(cls):
        return cls.objects.filter(status_emoji__in=EMOJI_MAPPING.values())

    @classmethod
    def mapped_statuses(cls, queryset, mapping=EMOJI_MAPPING):
        data = OrderedDict()
        for key, value in mapping.items():
            qs = queryset.filter(status_emoji=value)
            if qs.count() > 0:
                data[key] = {}
                data[key]['qs'] = qs
        return data

    @classmethod
    def get_user_presence(cls, queryset):
        slack_ids = queryset.values_list('slack_id', flat=True)
        scm = SlackClientMixin()
        for id in slack_ids:
            response = scm.slack_client.api_call(USERS['presence'], user=id)
            if response['ok']:
                presence = True if response['presence'] == 'active' else False
                cls.objects.filter(slack_id=id).update(is_online=presence)

    @classmethod
    def set_status(cls, slack_user_id, status_text, status_emoji):
        data = {
            'status_text': status_text,
            'status_emoji': status_emoji
        }
        scm = SlackClientMixin()
        scm.slack_client.api_call(
            USERS['set_profile'], user=slack_user_id, profile=data)


class ExternalApp(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    code = models.SlugField(_('Code'), max_length=30, unique=True)
    is_active = models.BooleanField(_('Is active'), default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('External app')
        verbose_name_plural = _('External apps')


class SlackUserExternalApp(models.Model):
    slack_user = models.ForeignKey(SlackUser, verbose_name=_('Slack user'))
    app = models.ForeignKey(ExternalApp, verbose_name=_('External app'))
    is_active = models.BooleanField(_('Is active'), default=True)
    username = models.CharField(_('Email/Username'), max_length=100)
    password = models.CharField(_('Password/Token'), max_length=100)

    def __str__(self):
        return '{0}-{1}'.format(self.app.name, self.slack_user.name)

    class Meta:
        verbose_name = _('External app for slack user')
        verbose_name_plural = _('External apps for slack users')
        unique_together = ('slack_user', 'app')
