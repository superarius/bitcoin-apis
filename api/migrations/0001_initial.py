# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-01 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DemoAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pubkey', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('privkey', models.CharField(max_length=500)),
            ],
        ),
    ]
