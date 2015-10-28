from django.db import models

class Pod(models.Model):

    name = models.CharField(max_length=50)

    host = models.OneToOneField('authentication.account', related_name='hosted_pod')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)

    @property
    def qr_code_url(self):
        return 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=%{}'.format(self.id)
