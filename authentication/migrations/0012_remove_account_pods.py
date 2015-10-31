# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_auto_20151031_2002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='pods',
        ),
    ]
