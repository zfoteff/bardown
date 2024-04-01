__version__ = "0.0.1"
__author__ = "Zac Foteff"

import datetime
from typing import Self

import mysql.connector as mysql

from src.logger import Logger

logger = Logger("mysql-client")


class MySQLClient:
    def __init__(self, config_map: dict) -> Self:
        self.__user = config_map["user"]
        self.__password = config_map["password"]
        self.__host = config_map["host"]
        self.__table = config_map["table"]
        self.__connection = mysql
        self.__cursor = None

    def open_connection(self) -> bool:
        logger.log(f"Attempting connection to {self.__table} . . .")
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
            logger.error(
                f"Database error when establishing connection: {err} . . . Quitting"
            )
            return False

    def close_connection(self) -> bool:
        """Save changes and close connection to database"""
        logger.log(f"Closing connection to {self.__table} . . .")
        try:
            self.__cursor.close()
            self.__connection.close()
            logger.log(f"Connection closed")
            return True
        except mysql.Error as err:
            logger.error(
                f"Database error when closing connection: {err} . . . Quitting"
            )

    """
    ====== PLAYER TABLE METHODS ======
    """

    def get_all_players(self) -> Tuple:
        query = """SELECT * FROM players"""

    """
    ====== STATISTICS TABLE METHODS ======
    """
