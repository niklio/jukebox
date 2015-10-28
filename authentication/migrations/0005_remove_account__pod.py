# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20151028_0300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='_pod',
        ),
    ]
