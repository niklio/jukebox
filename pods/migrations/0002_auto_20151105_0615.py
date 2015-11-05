# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pod',
            options={'permissions': set([('change_account_permissions', 'Can add or remove permissions from accounts in the pod.'), ('manage_pod', 'Can manage pod settings.'), ('remove_accounts', 'Can remove accounts from the pod.'), ('add_accounts', 'Can add accounts to the pod.')])},
        ),
    ]
