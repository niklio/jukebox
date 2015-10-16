from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile')
    pod = models.ForeignKey('pods.Pod', null=True, blank=True, related_name='members')

    username = models.CharField(max_length=50)
    email = models.EmailField()

    date_created = models.DateTimeField(auto_now_add=True)
    last_seen_on = models.DateTimeField(null=True, blank=True)

    @classmethod
    def create_profile(cls, user):
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            pass

        profile = cls()
        profile.user = user
        for attr in ('username', 'email'):
            setattr(profile, attr, getattr(user, attr))

        profile.save()
        return profile

    @property
    def is_host(self):
        return self.hosted_pod is not None
    