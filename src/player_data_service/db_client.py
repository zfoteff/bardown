__version__ = "0.0.1"
__author__ = "Zac Foteff"

from typing import Self, Tuple

import mysql.connector as mysql

from src.logger import Logger

logger = Logger("mysql-client")


class MySQLClient:
    def __init__(self, user: str, password: str, host: str, table: str) -> Self:
        self.__user = user
        self.__password = password
        self.__host = host
        self.__table = table
        self.__connection = mysql
        self.__database = "LaxDB"
        self.__cursor = None

    def open_connection(self) -> bool:
        logger.info(f"Attempting connection to {self.__table} at {self.__host} . . .")
        try:
            self.__connection = mysql.connect(
                user=self.__user,
                password=self.__password,
                host=self.__host,
                database=self.__database,
            )

            if self.__cursor == None:
                self.__cursor = self.__connection.cursor(buffered=True)
                logger.log("Successfully connected to database")
                return True

            logger.log("Found existing connection to the database")
            return True
        except mysql.Error as err:
            logger.error(
                f"Database error when establishing connection: {err} . . . Quitting"
            )
            return False

    def close_connection(self) -> bool:
        """Save changes and close connection to database"""
        logger.info(f"Closing connection to {self.__table} . . .")
        try:
            self.__cursor.close()
            self.__connection.close()
            logger.info(f"Connection closed")
            return True
        except mysql.Error as err:
            logger.error(
                f"Database error when closing connection: {err} . . . Quitting"
            )

    def execute_query(self, query: str) -> Tuple:
        logger.info(f"Executing query: {query}")
        try:
            self.__cursor.execute(query + ";")
            return (True, self.__cursor.fetchall())
        except mysql.Error as err:
            logger.error(f"Database error when running query: {err}")
            return (False, err)
