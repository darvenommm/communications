from rest_framework import status

from calls.models import Operator
from library.rest.api_status_test_case import ApiStatusTestCaseWrapper


class OperatorTestCase(ApiStatusTestCaseWrapper.ApiStatusTestCase):
    model = Operator
    entity_name = "operators"
    entity_data = {
        "title": "test_title",
        "description": "test_description",
        "foundation_date": "2000-03-23",
    }

    create_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
    change_put_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
    change_patch_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
    delete_statuses = (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN)
