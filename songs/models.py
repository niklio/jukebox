from django.db import models

from authentication.models import Account
from pods.models import Pod

class Song(models.Model):
    song_id = models.BigIntegerField()
    title = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)

    played = models.BooleanField(default=False)
    skip = models.BooleanField(default=False)

    pod = models.ForeignKey(
        Pod,
        related_name='songs',
        null=True
    )
    submitted_by = models.ForeignKey(
        Account,
        related_name='submitted_songs',
        null=True
    )

    def __unicode__(self):
        return self.title