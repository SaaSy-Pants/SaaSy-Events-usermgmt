from typing import Any

from app.models.organiser import Organiser
from app.services.service_factory import ServiceFactory
from framework.resources.base_resource import BaseResource


class OrganiserResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)

        self.data_service = ServiceFactory.get_service("UserResourceDataService") # We are using the same service for users and organisers
        self.database = "ORGANISER"
        self.collection = "org_tab"
        self.key_field="OID"

    def get_by_key(self, key: str) -> Organiser:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )

        return result

    def get_by_custom_key(self, custom_key: str, value: Any) -> Organiser:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=custom_key, key_value=value
        )

        return result

    def insert_data(self, organiser: Organiser):

        d_service = self.data_service

        result = d_service.insert_data_object(
            self.database, self.collection, organiser
        )

        return result

    def modify_data(self, organiser: Organiser):
        d_service = self.data_service

        result = d_service.modify_data_object(
            self.database, self.collection, organiser, self.key_field, organiser.OID
        )

        return result
