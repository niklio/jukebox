# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_auto_20151031_2003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='muted',
        ),
        migrations.AddField(
            model_name='membership',
            name='playing_songs',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
