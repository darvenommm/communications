from rest_framework import status

from library.ApiStatusTestCase import ApiStatusTestCaseWrapper


class UserTestCase(ApiStatusTestCaseWrapper.ApiStatusTestCase):
    entity_name = "users"
    entity_data = {
        "username": "username",
        "first_name": "first_name",
        "last_name": "last_name",
        "password": "password",
    }

    get_all_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
    get_one_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
    create_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
    change_put_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
    change_patch_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
    delete_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
