from django.db import models

from authentication.models import Account
from pods.models import Pod

class Song(models.Model):
    song_id = models.BigIntegerField()
    title = models.CharField(max_length=255)
    duration = models.BigIntegerField()

    stream_url = models.URLField()
    artwork_url = models.URLField()

    played = models.BooleanField(default=False)
    pod = models.ForeignKey(
        Pod,
        related_name='songs',
        null=True,
        on_delete=models.SET_NULL
    )
    submitted_by = models.ForeignKey(
        Account,
        related_name='submitted_songs',
        null=True,
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return self.title