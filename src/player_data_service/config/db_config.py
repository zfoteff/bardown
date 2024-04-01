import os
from typing import Dict

from dotenv import load_dotenv

load_dotenv()


def get_db_config(table: str) -> Dict[str, str]:
    return {
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "host": os.environ["DB_HOST"],
        "table": f"{table}",
    }
