# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User

from rest_framework import serializers

from users.models import SlackUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'slack_user')


class SlackUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = SlackUser
        fields = (
            'id', 'slack_id', 'team_id', 'name', 'real_name', 'avatar',
            'status_text', 'status_emoji', 'user')
