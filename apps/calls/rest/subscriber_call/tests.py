from typing import cast

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status, test

from calls.models import Subscriber
from library.ApiStatusTestCase import ApiStatusTestCaseWrapper


class SubscriberCallTestCase(ApiStatusTestCaseWrapper.ApiStatusTestCase):
    __user_data = {"first_name": "first_name", "last_name": "last_name", "password": "password"}

    __caller_user_data = {"username": "test_1", **__user_data}
    __caller_data = {"passport": "0000-000000", "birth_date": "2022-12-27"}

    __receiver_user_data = {"username": "test_2", **__user_data}
    __receiver_data = {"passport": "0000-000001", "birth_date": "2022-12-27"}

    @classmethod
    def setUpClass(cls) -> None:
        caller_user = get_user_model().objects.create(**cls.__caller_user_data)
        caller = Subscriber.objects.create(**cls.__caller_data, user=caller_user)
        caller_token = cast(Token, getattr(caller.user, "auth_token")).key

        receiver_user = get_user_model().objects.create(**cls.__receiver_user_data)
        receiver = Subscriber.objects.create(**cls.__receiver_data, user=receiver_user)

        cls.entity_data = {
            "caller": caller.pk,
            "receiver": receiver.pk,
            "start": "2022-12-27 08:26:49.219717",
            "duration": "1",
        }

        super().setUpClass()

        caller_client = test.APIClient()
        caller_client.login(
            username=cls.__caller_user_data["username"],
            password=cls.__caller_user_data["password"],
        )
        caller_client.credentials(HTTP_AUTHORIZATION=f"Token {caller_token}")

        cls.add_to_test_users(caller_client)

    entity_name = "subscribers_calls"

    get_all_statuses = (
        status.HTTP_403_FORBIDDEN,
        status.HTTP_200_OK,
        status.HTTP_200_OK,
    )
    get_one_statuses = (
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_200_OK,
    )
    create_statuses = (
        status.HTTP_403_FORBIDDEN,
        status.HTTP_403_FORBIDDEN,
        status.HTTP_403_FORBIDDEN,
    )
    change_put_statuses = (
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_403_FORBIDDEN,
    )
    change_patch_statuses = (
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_403_FORBIDDEN,
    )
    delete_statuses = (
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_403_FORBIDDEN,
    )
