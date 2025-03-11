from typing import List, Self, Tuple

import mysql.connector as mysql

from bin.logger import Logger

logger = Logger("mysql-client")


class MySQLClient:
    def __init__(self, user: str, password: str, host: str, table: str) -> Self:
        self.__user = user
        self.__password = password
        self.__host = host
        self.__table = table
        self.__connection = mysql
        self.__database = "LaxDB"

    def open_connection(
        self,
    ) -> bool:
        try:
            self.__connection = mysql.connect(
                user=self.__user,
                password=self.__password,
                host=self.__host,
                database=self.__database,
            )

            return True
        except mysql.Error as err:
            logger.error(
                f"""
                Database error when establishing connection to {self.__host}@{self.__database}:{self.__table}: {err} . . . Quitting
                """
            )
            return False

    def close_connection(self) -> bool:
        """Save changes and close connection to database"""
        logger.info(f"Closing connection to {self.__table} . . .")
        try:
            self.__connection.close()
            return True
        except mysql.Error as err:
            logger.error(f"Database error when closing connection: {err} . . . Quitting")
            return False

    def execute_query(
        self, query: str, commit_candidate: bool = False, return_results: bool = False
    ) -> Tuple[bool, List]:
        logger.debug(f"Executing query: {query}")
        data = []
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query + ";")
        except mysql.Error as err:
            logger.error(f"Database error when running query: {query}\nError:{err}")
            return (False, err)

        if commit_candidate:
            self.__connection.commit()

        if return_results:
            data = cursor.fetchall()

        return (True, data)
