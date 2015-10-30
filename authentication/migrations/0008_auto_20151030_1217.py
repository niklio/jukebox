# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0003_auto_20151028_0310'),
        ('authentication', '0007_auto_20151028_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='pod',
        ),
        migrations.AddField(
            model_name='account',
            name='pod',
            field=models.ManyToManyField(related_name='members', null=True, to='pods.Pod', blank=True),
        ),
    ]
