# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pods', '0003_auto_20151028_0310'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('song_id', models.BigIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('duration', models.BigIntegerField()),
                ('stream_url', models.URLField()),
                ('artwork_url', models.URLField()),
                ('played', models.BooleanField(default=False)),
                ('pod', models.ForeignKey(related_name='songs', on_delete=django.db.models.deletion.SET_NULL, to='pods.Pod', null=True)),
                ('submitted_by', models.ForeignKey(related_name='submitted_songs', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
