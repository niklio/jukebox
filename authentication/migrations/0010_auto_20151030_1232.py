# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_auto_20151030_1217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='pod',
            new_name='pods',
        ),
    ]
