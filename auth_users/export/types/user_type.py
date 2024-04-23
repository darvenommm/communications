from django.contrib.auth.models import AbstractUser


class UserType(AbstractUser):
    full_name: str

    class Meta:
        abstract = True
