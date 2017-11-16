
_speed = 1


def set_speed(speed: int) -> int:
    _speed = speed
    return _speed


def get_speed() -> int:
    return _speed


def goto_position(grade: int) -> int:
    pass


def get_position() -> int:
    pass


def increase_position(grade: int) -> int:
    goto_position(get_position() + grade)
    return get_position()


print("shit")
    # TODO: close pins met destructor
