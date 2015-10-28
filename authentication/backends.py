from django.contrib.auth.models import User

from authentication.models import Account

class AccountAuthBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            account = Account.objects.get(username=username)
            if account.check_password(password):
                return account
        except Account.DoesNotExist:
            return None

