# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0001_initial'),
        ('authentication', '0002_account_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='pod',
            field=models.ForeignKey(related_name='members', blank=True, to='pods.Pod', null=True),
        ),
    ]
