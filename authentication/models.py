from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.db import models

import datetime


class Membership(models.Model):
    pod = models.ForeignKey('pods.Pod')
    account = models.ForeignKey('Account')
    
    date_joined = models.DateField()
    invite_pending = models.BooleanField()


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):

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


class Account(AbstractBaseUser, PermissionsMixin):

    pods = models.ManyToManyField(
        'pods.Pod',
        related_name='members',
        blank=True,
        through=Membership
    )

    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username


# django-guardian
def get_anonymous_user_instance(User):
    return User(username='Anonymous', created_at=datetime.date(1970, 1, 1), updated_at=datetime.date(1970, 1, 1), email='')