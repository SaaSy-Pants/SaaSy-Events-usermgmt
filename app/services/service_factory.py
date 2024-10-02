from framework.services.data_access.MySqlRdbDataService import MySqlRdbDataService
from framework.services.service_factory import BaseServiceFactory


class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):
        if service_name == "UserResourceDataService":
            context = dict(user="root", password="dbuserdbuser",
                           host="localhost", port=3306)
            data_service = MySqlRdbDataService(context=context)
            return data_service
        else:
            return None