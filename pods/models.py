from django.db import models

class Pod(models.Model):

    name = models.CharField(max_length=50, unique=True)

    host = models.OneToOneField('authentication.account', related_name='hosted_pod')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)