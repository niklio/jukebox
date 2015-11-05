# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('song_id', models.BigIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('album', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('played', models.BooleanField(default=False)),
                ('skip', models.BooleanField(default=False)),
                ('pod', models.ForeignKey(related_name='songs', to='pods.Pod', null=True)),
                ('submitted_by', models.ForeignKey(related_name='submitted_songs', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
