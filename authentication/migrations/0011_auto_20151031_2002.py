# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0003_auto_20151028_0310'),
        ('authentication', '0010_auto_20151030_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateField()),
                ('permissions', multiselectfield.db.fields.MultiSelectField(max_length=11, choices=[(b'AU', b'Add users'), (b'MU', b'Manage users'), (b'MP', b'Manage pod'), (b'VT', b'Vote')])),
                ('muted', models.BooleanField()),
                ('invite_pending', models.BooleanField()),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('pod', models.ForeignKey(to='pods.Pod')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='pods_temp',
            field=models.ManyToManyField(related_name='members_temp', through='authentication.Membership', to='pods.Pod', blank=True),
        ),
    ]
