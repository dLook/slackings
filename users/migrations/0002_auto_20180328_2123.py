# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-28 21:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('code', models.SlugField(max_length=30, unique=True, verbose_name='Code')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
            ],
            options={
                'verbose_name': 'External app',
                'verbose_name_plural': 'External apps',
            },
        ),
        migrations.CreateModel(
            name='SlackUserExternalApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('username', models.CharField(max_length=100, verbose_name='Email/Username')),
                ('password', models.CharField(max_length=100, verbose_name='Password/Token')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.ExternalApp', verbose_name='External app')),
                ('slack_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.SlackUser', verbose_name='Slack user')),
            ],
            options={
                'verbose_name': 'External app for slack user',
                'verbose_name_plural': 'External apps for slack users',
            },
        ),
        migrations.AlterUniqueTogether(
            name='slackuserexternalapp',
            unique_together=set([('slack_user', 'app')]),
        ),
    ]
