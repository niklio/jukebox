from django.db import models
from users.models import UserProfile

class Pod(models.Model):
    host = models.ForeignKey(UserProfile, related_name='hosted_pod')
    date_created = models.DateTimeField()