from typing import Union


def clamp(val, minimum, maximum):
    return max(minimum, min(maximum, val))


def clamp_alpha(alpha: Union[int, float]):
    return clamp(int(alpha), 0, 255)
