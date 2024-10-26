from typing import Any

from app.models.organiser import Organiser
from app.services.service_factory import ServiceFactory
from framework.resources.base_resource import BaseResource

import pymysql

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

        connection = pymysql.connect(
            host = d_service.context['host'],
            user = d_service.context['user'],
            password = d_service.context['password'],
            port = d_service.context['port'],
            database = self.database
        )

        result = {
            'status': "Connection Unsuccessful",
            'error': "DB Connection Error"
        }

        if connection is not None:

            updated_organiser_data = {
                "Name": organiser.Name,
                "Email": organiser.Email,
                "PhoneNo": organiser.PhoneNo,
                "HashedPswd": organiser.HashedPswd,
                "Address": organiser.Address,
                "Age": organiser.Age
            }


            set_clause = ", ".join([f"{key} = '{value}'" for key, value in updated_organiser_data.items()])
            query = f"UPDATE {self.collection} SET {set_clause} WHERE {self.key_field} = '{organiser.OID}'"

            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                updated_count = cursor.rowcount

                if updated_count == 0:
                    result['error'] = 'Corrupt OID passed'
                    result['status'] = "Organiser Modification Failed"
                else:
                    result['error'] = None
                    result['status'] = 'Organiser Modification Successful'


        return result
