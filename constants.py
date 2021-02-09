import enum


class RotorDirections(enum.Enum):
    CLOCKWISE = 1
    ANTI_CLOCKWISE = -1


class CurrentFlowDirections(enum.Enum):
    FORWARD = 1
    REVERSE = -1
