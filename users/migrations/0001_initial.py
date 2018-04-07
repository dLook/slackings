# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-26 23:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SlackUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_id', models.CharField(max_length=20, unique=True, verbose_name='Slack ID')),
                ('team_id', models.CharField(max_length=20, verbose_name='Slack team ID')),
                ('name', models.CharField(max_length=100, verbose_name='Slack name')),
                ('real_name', models.CharField(max_length=100, verbose_name='Slack real name')),
                ('avatar', models.URLField(blank=True, default='', max_length=255, verbose_name='Slack avatar')),
                ('status_text', models.CharField(blank=True, default='', max_length=255, verbose_name='Slack status text')),
                ('status_emoji', models.CharField(blank=True, default='', max_length=100, verbose_name='Slack status emoji')),
                ('is_online', models.BooleanField(default=False, verbose_name='Is online')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slack_user', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ('-last_modified',),
                'verbose_name': 'Slack user',
                'verbose_name_plural': 'Slack users',
            },
        ),
        migrations.AlterUniqueTogether(
            name='slackuser',
            unique_together=set([('slack_id', 'team_id')]),
        ),
    ]
