# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_account_pod'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='pod',
            new_name='_pod',
        ),
    ]
