from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('Users must have a valid username')

        email_for_jwt = username + '@forjwt.com'

        account = self.model(
            username = username,
            email = email_for_jwt
        )

        account.set_password(password)
        account.save()

        return account


    def create_superuser(self, username, password, **kwargs):
        account = self.create_user(username, password, **kwargs)

        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    
    pods = models.ManyToManyField(
        'pods.Pod',
        related_name='members',
        blank=True
    )

    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'

    @property
    def is_host(self):
        return hasattr(self, 'hosted_pod') or False

    def __unicode__(self):
        return self.username
    
    