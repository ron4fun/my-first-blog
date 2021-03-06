from django.conf import settings
from django.contrib.auth.models import check_password
from .models import User

class UserAuthBackend(object):
    """
    A custom authentication backend.
    Allows users to log in using their username.
    """

    def authenticate(self, username=None, password=None):
        """
        Authentication method
        """
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
            
