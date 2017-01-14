# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('access_token_granted', models.BooleanField(default=False)),
                ('alias', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('code', models.CharField(max_length=6)),
                ('verified', models.BooleanField(default=False)),
                ('secret_identifier', models.CharField(blank=True, max_length=48)),
                ('expiry', models.DateTimeField(null=True)),
            ],
        ),
    ]