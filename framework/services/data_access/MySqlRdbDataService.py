import pymysql
from pydantic import BaseModel
from pymysql import MySQLError

from .BaseDataService import BaseDataService


class MySqlRdbDataService(BaseDataService):
    """
    A generic data service for MySQL databases. The class implement common
    methods from BaseDataService and other methods for MySQL. More complex use cases
    can subclass, reuse methods and extend.
    """

    def __init__(self, context):
        super().__init__(context)

    def _get_connection(self):
        connection = pymysql.connect(
            host = self.context["host"],
            port = self.context["port"],
            user = self.context["user"],
            password = self.context["password"],
            cursorclass = pymysql.cursors.DictCursor,
            autocommit = True
        )
        return connection

    def check_connection(self, database_name: str, table_name: str):
        """
        Check if the connection to the database is successful by selecting all data
        from a specific table.
        Args:
            - database_name: Name of the database to query.
            - table_name: Name of the table to fetch all records from.
        Returns:
            - A dictionary with connection status and result of the query (all rows).
        Raises:
            - Exception if the connection or query execution fails.
        """
        connection = None
        try:
            # Establish a connection
            connection = self._get_connection()

            # Create a cursor and execute a query to select all rows from the given table
            cursor = connection.cursor()
            query = f"SELECT * FROM {database_name}.{table_name}"
            cursor.execute(query)

            # Fetch all the results (each row will be a dictionary)
            result = cursor.fetchall()

            # Return the result
            if connection.open:
                return {"status": "connection is live", 'data': result }
            else:
                return {"status": "connection failed"}

        except MySQLError:
            return {"status": "connection failed"}

        finally:
            # Ensure the connection is closed after the check
            if connection and connection.open:
                connection.close()

    def insert_data_object(
        self,
        database_name: str,
        collection_name: str,
        data_model: BaseModel
    ):
        """
        See base class for comments.
        """

        connection = None
        try:
            # Extract field names and values from the BaseModel
            fields = ', '.join(data_model.model_dump().keys())
            placeholders = ', '.join(['%s'] * len(data_model.model_dump()))
            values = tuple(data_model.model_dump().values())

            # Dynamically construct the SQL query
            sql_statement = f"INSERT INTO {database_name}.{collection_name} ({fields}) VALUES ({placeholders})"

            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, values)

            return {"status": "inserted successfully", "error": None}

        except Exception as e:
            if connection is None:
                result = {"status": "internal server error ", "error": str(e)}
            else:
                result = {"status": "bad request", "error": str(e)}

            if connection and connection.open:
                connection.close()

            return result

    def get_data_object(
        self,
        database_name: str,
        collection_name: str,
        key_field: str,
        key_value: str
    ):
        """
        See base class for comments.
        """

        connection = None
        try:
            sql_statement = f"SELECT * FROM {database_name}.{collection_name} " + \
                        f"where {key_field}=%s"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [key_value])
            result = cursor.fetchone()

        except Exception as e:
            if connection and connection.open:
                connection.close()
            result = {"status": "failed", "error": str(e)}

        return result

    def modify_data_object(
            self,
            database_name: str,
            collection_name: str,
            data_model: BaseModel,
            key_field=str,
            key_value=str
    ):

        connection = None
        try:
            set_clause = ", ".join([f"{key} = '{value}'" for key, value in data_model.model_dump().items()])
            sql_statement = f"UPDATE {database_name}.{collection_name} SET {set_clause} WHERE {key_field}=%s"
            try:
                connection = self._get_connection()
                cursor = connection.cursor()
                cursor.execute(sql_statement, [key_value])  # not throwing error
                updated_count = cursor.rowcount
                if updated_count == 0:
                    result =  {"status": "bad request", "error": f"{key_field} does not exist"}
                else:
                    result =  {"status": "modification successful", "error": None}

                return result
            except Exception as e:
                return {"status": "bad request", "error": str(e)}

        except Exception as e:
            if connection is None:
                result = {"status": "internal server error ", "error": str(e)}
                return result

            if connection and connection.open:
                connection.close()



