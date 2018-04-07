# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User

from rest_framework import viewsets

from users.models import SlackUser
from .serializers import UserSerializer, SlackUserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True, is_staff=False)
    serializer_class = UserSerializer


class SlackUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SlackUser.objects.all()
    serializer_class = SlackUserSerializer
