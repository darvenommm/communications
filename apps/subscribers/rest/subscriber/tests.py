from rest_framework import status

from subscribers.models import Subscriber
from library.rest.api_status_test_case import ApiStatusTestCaseWrapper


class SubscriberTestCase(ApiStatusTestCaseWrapper.ApiStatusTestCase):
    queryset = Subscriber.objects.all()
    entity_name = "subscribers"
    entity_data = {
        "username": "username",
        "first_name": "first_name",
        "last_name": "last_name",
        "password": "password",
    }

    get_all_statuses = (status.HTTP_200_OK, status.HTTP_200_OK)
    get_one_statuses = (status.HTTP_200_OK, status.HTTP_200_OK)
    create_statuses = (status.HTTP_201_CREATED, status.HTTP_201_CREATED)
    change_put_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_200_OK)
    change_patch_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_200_OK)
    delete_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_204_NO_CONTENT)
