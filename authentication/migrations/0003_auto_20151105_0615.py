# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20151105_0524'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([]),
        ),
    ]
