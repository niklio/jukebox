# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('pods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pod',
            name='host',
            field=models.OneToOneField(related_name='hosted_pod', default='', to='accounts.UserProfile'),
            preserve_default=False,
        ),
    ]
