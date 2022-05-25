from enum import Enum


class Permission:
    SEE = 1
    SEE_ALL = 2
    ADMIN = 16


class ScheduleRegularType(Enum):
    NEW = 0
    OLD = 1
    RANDOM = 2


class FlashType(Enum):
    INFO = "info"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    ERROR = "danger"
    WARNING = "warning"
    LIGHT = "light"
    DARK = "dark"
