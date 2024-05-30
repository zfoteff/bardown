from enum import Enum


class Grade(Enum):
    FRESHMAN = "FR"
    SOPHOMORE = "SO"
    JUNIOR = "JR"
    SENIOR = "SR"

    def __str__(self) -> str:
        return str.capitalize(self.name)
