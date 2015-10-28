# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0002_auto_20151028_0301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pod',
            old_name='_host',
            new_name='host',
        ),
    ]
