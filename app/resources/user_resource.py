from typing import Any

from framework.resources.base_resource import BaseResource

from app.models.user import User
from app.services.service_factory import ServiceFactory

class UserResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)

        self.data_service = ServiceFactory.get_service("UserResourceDataService")
        self.database = "USER"
        self.collection = "user_tab"
        self.key_field="UID"

    def get_by_key(self, key: str) -> User:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )

        return result

    def get_by_custom_key(self, custom_key: str, value: Any) -> User:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=custom_key, key_value=value
        )

        return result

    def insert_data(self, user: User):

        d_service = self.data_service

        result = d_service.insert_data_object(
            self.database, self.collection, user
        )

        return result

    def modify_data(self, user: User):

        d_service = self.data_service

        result = d_service.modify_data_object(
            self.database, self.collection, user, self.key_field, user.UID
        )

        return result
