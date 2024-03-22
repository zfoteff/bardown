import datetime
from typing import Self

import mysql.connector as mysql

from src.logger import Logger

logger = Logger("mysql-client")


class MySQLClient:
    def __init__(self, config_map: dict) -> Self:
        self.__user = ""
        self.__password = ""
        self.__host = ""
        self.__table = ""
        self.__connection = mysql
        self.__cursor = None

    def open_connection(self) -> bool:
        logger.log("Attempting DB connection . . .")
        try:
            self.__connection = mysql.connect(
                user=self.__user,
                password=self.__password,
                host=self.__host,
                database=self.__table,
            )

            if self.__cursor != None:
                self.__cursor = self.__connection.cursor(buffered=True)
                logger.log("Successfully connected to database")
                return True

            logger.log("Found existing connection to the database")
            return True
        except mysql.Error as err:
            logger.error(f"Database error {err} . . . Quitting")
            return False

    def close_connection(self) -> None:
        """Save changes and close connection to database"""
        self.__cursor.close()
        self.__connection.close()
        logger.log(f"Connection closed")
