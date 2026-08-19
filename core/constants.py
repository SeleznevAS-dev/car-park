from enum import StrEnum


class DriveType(StrEnum):
    FWD = "Передний"
    RWD = "Задний"
    AWD = "Полный"


class FuelType(StrEnum):
    PETROL = "Бензин"
    DIESEL = "Дизель"
    GAS = "Газ"


UserIdType = int
