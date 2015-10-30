# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='artwork_url',
        ),
        migrations.RemoveField(
            model_name='song',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='song',
            name='stream_url',
        ),
        migrations.AddField(
            model_name='song',
            name='album',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='artist',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='skip',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='song',
            name='pod',
            field=models.ForeignKey(related_name='songs', to='pods.Pod', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='submitted_by',
            field=models.ForeignKey(related_name='submitted_songs', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
