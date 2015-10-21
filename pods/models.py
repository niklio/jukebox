from django.db import models
from accounts.models import UserProfile

class Pod(models.Model):

    name = models.CharField(max_length=50)
    host = models.OneToOneField(UserProfile, related_name='hosted_pod')
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def qr_code_url(self):
        return 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=%s' % self.id