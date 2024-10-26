from typing import Any

from framework.resources.base_resource import BaseResource

from app.models.user import User
from app.services.service_factory import ServiceFactory
import pymysql

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

            updated_user_data = {
                "Name": user.Name,
                "Email": user.Email,
                "PhoneNo": user.PhoneNo,
                "HashedPswd": user.HashedPswd,
                "Address": user.Address,
                "Age": user.Age
            }


            set_clause = ", ".join([f"{key} = '{value}'" for key, value in updated_user_data.items()])
            query = f"UPDATE {self.collection} SET {set_clause} WHERE {self.key_field} = '{user.UID}'"

            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                updated_count = cursor.rowcount

                if updated_count == 0:
                    result['error'] = 'Corrupt UID passed'
                    result['status'] = "User Modification Failed"
                else:
                    result['error'] = None
                    result['status'] = 'User Modification Successful'


        return result
