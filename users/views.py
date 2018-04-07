# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView

from common.views import SlackEventListener
from .forms import ConnectExternalAppFrom
from .models import SlackUser, ExternalApp, SlackUserExternalApp


class UserChangeEventListener(SlackEventListener):
    def handle_user_change(self, slack_json):
        data = SlackUser.extract_data_from_slack(slack_json)
        SlackUser.objects.filter(slack_id=data.get('slack_id')).update(**data)


class SlackUserStatusGridView(TemplateView):
    template_name = 'users/status_grid.html'
    http_method_names = ['get']

    def dispatch(self, request, *args, **kwargs):
        self.queryset = SlackUser.get_all_with_important_statuses()
        SlackUser.get_user_presence(self.queryset)
        return super(SlackUserStatusGridView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SlackUserStatusGridView, self).get_context_data(**kwargs)
        context.update({
            'mapped_statuses': SlackUser.mapped_statuses(self.queryset)
        })
        return context


class ConnectExternalAppFormView(FormView):
    form_class = ConnectExternalAppFrom
    template_name = 'users/connect_external_app_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.app = ExternalApp.objects.get(id=kwargs.get('app_id'))
        self.slack_user = SlackUser.objects.get(id=kwargs.get('slack_user_id'))
        return super(ConnectExternalAppFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        SlackUserExternalApp.objects.update_or_create(
            slack_user=self.slack_user, app=self.app, defaults=form.cleaned_data)
        return super(ConnectExternalAppFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:connect_external_app_success')


class ConnectExternalAppSuccessView(TemplateView):
    template_name = 'users/connect_external_app_success.html'
