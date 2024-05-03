from django.contrib.auth.models import AbstractUser

from rest_framework.authtoken.models import Token


class UserType(AbstractUser):
    full_name: str
    auth_token: Token

    class Meta:
        abstract = True
