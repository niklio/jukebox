# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pod',
            name='host',
            field=models.ForeignKey(related_name='hosted_pod', to='users.UserProfile'),
        ),
    ]
