def is_int(inp: str) -> bool:
    try:
        int(inp)
        return True
    except ValueError:
        return False
