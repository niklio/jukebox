from django.db import models

class Pod(models.Model):

    host = models.ForeignKey('accounts.UserProfile', related_name='hosted_pod')
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.host) +"'s Pod"

    @property
    def qr_code_url(self):
        return 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=%s' % self.id

    def save(self, *args, **kwargs):
        created = not self.id
        super(Pod, self).save(*args, **kwargs)

        if created:
          host = self.host
          host.pod = self
          host.save()