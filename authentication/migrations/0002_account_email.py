# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='email',
            field=models.EmailField(default='placeholder', max_length=254),
            preserve_default=False,
        ),
    ]