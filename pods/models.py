from django.db import models
from users.models import UserProfile

class Pod(models.Model):

    host = models.ForeignKey(UserProfile, related_name='hosted_pod')

    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Pod, self).save(*args, **kwargs)

        if not self.id:
            host, host.pod = self.host, self
            host.save()
