from django.db import models

from authentication.models import Account

class Pod(models.Model):

    name = models.CharField(max_length=50, unique=True, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        permissions = {
            ('add_accounts', 'Can add accounts to the pod.'),
            ('remove_accounts', 'Can remove accounts from the pod.'),
            ('change_account_permissions', 'Can add or remove permissions from accounts in the pod.'),
            ('manage_pod', 'Can manage pod settings.'),
            # ('delete_pod', 'Can delete the pod.'),
        }