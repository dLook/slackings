# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .settings import EVENTS


class SlackEventListener(View):
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        self.data = json.loads(request.body)
        self.token = self.data.get('token')
        self.event_type = self.data.get('type')
        return super(SlackEventListener, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if self.event_type == EVENTS['TYPES']['callback']:
            event = self.data.get('event')
            if event:
                EVENTS['SUBSCRIBED'].get(event['type'])(self)(event.get('user'))
            return HttpResponse(status=200, content='OK')
        elif self.event_type == EVENTS['TYPES']['verification']:
            content = json.dumps({'challenge': '{0}'.format(self.data.get('challenge'))})
            return HttpResponse(status=200, content=content, content_type='application/json')
        return HttpResponse(status=500, content='Unsupported event!')
