from rest_framework import status

from library.ApiStatusTestCase import ApiStatusTestCaseWrapper


class SubscriberTestCase(ApiStatusTestCaseWrapper.ApiStatusTestCase):
    entity_name = "subscribers"
    entity_data = {
        "passport": "0000-000000",
        "birth_date": "2000-03-23",
        "user": {
            "username": "username",
            "first_name": "first_name",
            "last_name": "last_name",
            "password": "password",
            "email": "email@gmail.com",
        },
        "operators": [],
    }

    change_put_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
    change_patch_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
    delete_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
