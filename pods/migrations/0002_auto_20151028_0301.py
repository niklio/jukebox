# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pod',
            old_name='host',
            new_name='_host',
        ),
        migrations.AlterField(
            model_name='pod',
            name='name',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
