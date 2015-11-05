# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('pod', 'account')]),
        ),
        migrations.RemoveField(
            model_name='membership',
            name='playing_songs',
        ),
    ]
