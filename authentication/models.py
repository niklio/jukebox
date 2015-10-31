from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models

from multiselectfield import MultiSelectField

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


class Membership(models.Model):
    pod = models.ForeignKey('pods.Pod')
    account = models.ForeignKey('Account')
    date_joined = models.DateField()

    ADD_SONGS = 'AS'
    MANAGE_SONGS = 'MS'
    ADD_USERS = 'AU'
    MANAGE_USERS = 'MU'
    MANAGE_POD = 'MP'
    VOTE = 'VT'

    PERMISSIONS_CHOICES = (
        (ADD_SONGS, 'Add songs'),
        (MANAGE_SONGS, 'Manage songs'),
        (ADD_USERS, 'Add users'),
        (MANAGE_USERS, 'Manage users'),
        (MANAGE_POD, 'Manage pod'),
        (VOTE, 'Vote')
    )

    permissions = MultiSelectField(choices=PERMISSIONS_CHOICES)
    invite_pending = models.BooleanField()
    playing_songs = models.BooleanField()

class Account(AbstractBaseUser):

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
