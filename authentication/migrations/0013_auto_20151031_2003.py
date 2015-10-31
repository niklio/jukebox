# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0003_auto_20151028_0310'),
        ('authentication', '0012_remove_account_pods'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='pods_temp',
        ),
        migrations.AddField(
            model_name='account',
            name='pods',
            field=models.ManyToManyField(related_name='members', through='authentication.Membership', to='pods.Pod', blank=True),
        ),
    ]
