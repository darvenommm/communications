"""Subscriber call test case module."""

from typing import cast

from calls.models import SubscriberCall
from rest_framework import status, test
from rest_framework.authtoken.models import Token
from subscribers.models import Subscriber

from library.rest.api_status_test_case import ApiStatusTestCaseWrapper


class SubscriberCallTestCase(ApiStatusTestCaseWrapper.ApiStatusTestCase):
    """Subscriber call test case."""

    __user_data = {"first_name": "first_name", "last_name": "last_name", "password": "password"}

    __caller_data = {
        "username": "test_1",
        "passport": "0000-000000",
        "birth_date": "2022-12-27",
        **__user_data,
    }
    __receiver_data = {
        "username": "test_2",
        "passport": "0000-000001",
        "birth_date": "2022-12-27",
        **__user_data,
    }

    model = SubscriberCall
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

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class.

        Raises:
            ValueError: not login.
        """
        caller = Subscriber(**cls.__caller_data)
        caller.set_password(cls.__caller_data["password"])
        caller.save()
        caller_token = cast(Token, getattr(caller, "auth_token")).key

        receiver = Subscriber(**cls.__receiver_data)
        receiver.set_password(cls.__receiver_data["password"])
        receiver.save()

        cls.entity_data = {
            "caller": str(caller.id),
            "receiver": str(receiver.id),
            "start": "2022-12-27 08:26:49.219717",
            "duration": "1",
        }

        super().setUpClass()

        caller_client = test.APIClient()
        is_login = caller_client.login(
            username=cls.__caller_data["username"],
            password=cls.__caller_data["password"],
        )

        if not is_login:
            raise ValueError("Caller client is not login")

        caller_client.credentials(HTTP_AUTHORIZATION=f"Token {caller_token}")

        cls.add_to_test_users(caller_client)
