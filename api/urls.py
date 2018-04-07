# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SlackUserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'slack-users', SlackUserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
