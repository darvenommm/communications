from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status

from calls.models import Subscriber
from calls.rest.mixins.tests import ApiTestMixinWrapper


class SubscriberCallTestCase(ApiTestMixinWrapper.ApiTestMixin, TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        caller = Subscriber.objects.create(
            passport="0000-000000",
            birth_date="2022-12-27",
            user=get_user_model().objects.create(
                username="test_1",
                first_name="first_name",
                last_name="last_name",
                email="email@gmail.com",
            ),
        )

        receiver = Subscriber.objects.create(
            passport="1111-111111",
            birth_date="2022-12-27",
            user=get_user_model().objects.create(
                username="test_2",
                first_name="first_name",
                last_name="last_name",
                email="email@gmail.com",
            ),
        )

        cls.entity_data = {
            "caller": caller.pk,
            "receiver": receiver.pk,
            "start": "2022-12-27 08:26:49.219717",
            "duration": "1",
        }

        return super().setUpClass()

    entity_name = "subscribers_calls"

    get_all_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_200_OK)
    get_one_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND)
    create_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
    change_put_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND)
    change_patch_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND)
    delete_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND)
