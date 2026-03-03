import math
from enum import Enum

class Method(Enum):
    LINEAR = 1
    CONSTANT = 2
    CUBIC = 3
    SINE = 4
    BOUNCE = 5
class Direction(Enum):
    INOUT = 1
    IN = 2
    OUT = 3

def interpolate(position: float, method: Method, direction: Direction) -> float:
    """Returns a float from 0.0 to 1.0 using an interpolation style and direction.

    Args:
        position (float): X position (0.0 to 1.0)
        style (Style): Interpolation style (Linear, Ease, etc)
        direction (Direction): Interpolation direction (In-Out, In, Out)

    Returns:
        float: Y (0.0 to 1.0)
    """
    position = max(min(position, 1.0), 0.0)
    if not isinstance(method, Method):
        raise TypeError("Invalid Enum for method")
    if not isinstance(direction, Direction):
        raise TypeError("Invalid Enum for direction")
    match method:
        case Method.LINEAR:
            return position
        case Method.CONSTANT:
            return float(position == 1.0)
        case Method.CUBIC:
            match direction:
                case Direction.INOUT:
                    return 4 * (position ** 3) if position < 0.5 else 0.5 + ((1.0 - ((-2 * position + 2) ** 3)) / 2)
                case Direction.IN:
                    return position ** 3
                case Direction.OUT:
                    return 1 - ((1 - position) ** 3)
                case _:
                    return -1.0
        case Method.SINE:
            match direction:
                case Direction.INOUT:
                    return -(math.cos(math.pi * position) - 1) / 2
                case Direction.IN:
                    return 1 - math.cos((position * math.pi) / 2)
                case Direction.OUT:
                    return math.sin((position * math.pi) / 2)
                case _:
                    return 0.0
        case Method.BOUNCE:
            def easeOutBounce(x: float) -> float:
                n1 = 7.5625
                d1 = 2.75

                if x < 1 / d1:
                    return n1 * x * x
                elif x < 2 / d1:
                    x -= 1.5 / d1
                    return n1 * x * x + 0.75
                elif x < 2.5 / d1:
                    x -= 2.25 / d1
                    return n1 * x * x + 0.9375
                else:
                    x -= 2.625 / d1
                    return n1 * x * x + 0.984375
            def easeInOutBounce(x: float) -> float:
                if x < 0.5:
                    return (1 - easeOutBounce(1 - 2 * x)) / 2
                else:
                    return (1 + easeOutBounce(2 * x - 1)) / 2
            def easeInBounce(x: float) -> float:
                return 1 - easeOutBounce(1 - x)
            match direction:
                case Direction.INOUT:
                    return easeInOutBounce(position)
                case Direction.IN:
                    return easeInBounce(position)
                case Direction.OUT:
                    return easeOutBounce(position)
                case _:
                    return 0.0

        case _:
            return 0.0
