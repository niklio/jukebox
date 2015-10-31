from django.db import models

from authentication.models import Account

class Pod(models.Model):

    name = models.CharField(max_length=50, unique=True, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)