def triangle_number(inp: int) -> int:
    return int((inp ** 2 / 2) + (inp / 2))


def wrap(num: int, mod: int) -> int:
    """
    This is like modulo, but plus one.
    :param num: Number to wrap
    :param mod: Maximum output to allow
    :return: The input number, wrapped by the mod number
    """
    return 1 + ((num - 1) % mod)
