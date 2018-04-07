# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .logic import VacationHelper


class VacationRecordView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(VacationRecordView, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        content = VacationHelper.process(request.POST)
        return HttpResponse(content=content, status=200)
