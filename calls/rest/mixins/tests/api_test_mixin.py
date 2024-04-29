from typing import cast, TypeAlias, Optional, Literal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import test, status
from rest_framework.response import Response

from auth_users.export.types import UserType


HttpStatusesType: TypeAlias = tuple[int, int]
VariantOfTestType: TypeAlias = (
    Literal["get_all"]
    | Literal["get_one"]
    | Literal["post"]
    | Literal["put"]
    | Literal["patch"]
    | Literal["delete"]
)


# without wrapper this mixin class that be executed
class ApiTestMixinWrapper:
    class ApiTestMixin(TestCase):
        entity_name: str
        entity_data: dict

        get_all_statuses: HttpStatusesType = (status.HTTP_200_OK, status.HTTP_200_OK)
        get_one_statuses: HttpStatusesType = (status.HTTP_200_OK, status.HTTP_200_OK)
        create_statuses: HttpStatusesType = (status.HTTP_201_CREATED, status.HTTP_201_CREATED)
        change_put_statuses: HttpStatusesType = (status.HTTP_200_OK, status.HTTP_200_OK)
        change_patch_statuses: HttpStatusesType = (status.HTTP_200_OK, status.HTTP_200_OK)
        delete_statuses: HttpStatusesType = (status.HTTP_204_NO_CONTENT, status.HTTP_204_NO_CONTENT)

        __user_data = {
            field: field for field in ("first_name", "last_name", "username", "password")
        }

        @classmethod
        def setUpClass(cls) -> None:
            cls.anonym = test.APIClient()

            authorized_user = cast(
                UserType,
                get_user_model().objects.create(**cls.__create_unique_user_data("authorized")),
            )
            cls.authorized = test.APIClient()
            cls.authorized.force_authenticate(authorized_user, authorized_user.auth_token.key)

            admin_user = cast(
                UserType,
                get_user_model().objects.create(**cls.__create_unique_user_data("admin")),
            )
            admin_user.is_staff = True
            cls.admin = test.APIClient()
            cls.admin.force_authenticate(admin_user, admin_user.auth_token.key)

            cls.test_users = (cls.anonym, cls.authorized)

            super().setUpClass()

        def test_get_all(self) -> None:
            entities_url = self.__create_url()

            for index, test_user in enumerate(self.test_users):
                response = cast(Response, test_user.get(entities_url))
                self.assertEqual(response.status_code, self.get_all_statuses[index])

        def test_get_one(self) -> None:
            entity_url = self.__create_entity()

            for index, test_user in enumerate(self.test_users):
                response = cast(Response, test_user.get(entity_url))
                self.assertEqual(response.status_code, self.get_one_statuses[index])

        def test_create(self) -> None:
            entity_url = self.__create_url()

            for index, test_user in enumerate(self.test_users):
                response = cast(Response, test_user.post(entity_url, self.entity_data))
                self.assertEqual(response.status_code, self.create_statuses[index])

        def test_put_update(self) -> None:
            entity_url = self.__create_entity()

            for index, test_user in enumerate(self.test_users):
                response = cast(Response, test_user.put(entity_url, self.entity_data))
                self.assertEqual(response.status_code, self.change_put_statuses[index])

        def test_patch_update(self) -> None:
            entity_url = self.__create_entity()

            for index, test_user in enumerate(self.test_users):
                response = cast(Response, test_user.patch(entity_url, self.entity_data))
                self.assertEqual(response.status_code, self.change_patch_statuses[index])

        def test_delete_update(self) -> None:
            entity_url = self.__create_entity()

            for index, test_user in enumerate(self.test_users):
                response = cast(Response, test_user.delete(entity_url, self.entity_data))
                self.assertEqual(response.status_code, self.delete_statuses[index])

        @classmethod
        def __create_unique_user_data(cls, unique_name: str) -> dict[str, str]:
            return {
                field_key: f"{cls.__name__}_{unique_name}_{field_value}"
                for field_key, field_value in cls.__user_data.items()
            }

        def __create_url(self, entity_pk: Optional[str] = None) -> str:
            base_url = cast(str, settings.REST_FRAMEWORK_API_PATH).strip("/")
            entity_name = self.entity_name.strip("/")

            entities_url = f"/{base_url}/{entity_name}/"

            return entities_url if not entity_pk else f"{entities_url}{entity_pk}/"

        def __create_entity(self) -> str:
            base_url = self.__create_url()
            response = cast(Response, self.admin.post(base_url, self.entity_data))

            return self.__create_url(cast(dict, response.json()).get("id"))
