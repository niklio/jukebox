# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'permissions': set([('delete_pod', 'Can delete the pod.'), ('manage_pod', 'Can manage pod settings.'), ('remove_user', 'Can remove users from the pod.'), ('change_user_permissions', 'Can add or remove permissions from users in the pod.'), ('add_user', 'Can add users to the pod.')]),
            },
        ),
    ]
