# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0003_auto_20151028_0310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pod',
            options={'permissions': set([('add_user', 'Can add users to the pod.'), ('manage_pod', 'Can manage pod settings.'), ('remove_user', 'Can remove users from the pod.'), ('change_user_permissions', 'Can add or remove permissions from users in the pod.')])},
        ),
        migrations.RemoveField(
            model_name='pod',
            name='host',
        ),
    ]
