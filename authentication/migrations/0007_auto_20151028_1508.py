# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_account_pod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pod',
            field=models.ForeignKey(related_name='members', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='pods.Pod', null=True),
        ),
    ]
