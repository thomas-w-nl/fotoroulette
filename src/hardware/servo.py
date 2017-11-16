_position = 0


def goto_position(graden: int):
    _position = graden


def get_position() -> int:
    pass


def increase_position(graden: int) -> int:
    goto_position(get_position() + graden)
    return get_position()
