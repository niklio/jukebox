# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20151030_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pod',
            field=models.ManyToManyField(related_name='members', to='pods.Pod', blank=True),
        ),
    ]
