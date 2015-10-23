from django.db import models

class Pod(models.Model):

    host = models.OneToOneField('accounts.UserProfile', related_name='hosted_pod')
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode(self.name)

    @property
    def qr_code_url(self):
        return 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=%s' % self.id