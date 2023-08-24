from nicegui import ui
from contextlib import contextmanager


@contextmanager
def disable_element(element) -> None:
    element.disable()
    try:
        yield
    finally:
        element.enable()


def is_str_empty(label: str, value: str) -> bool:
    ret = value is None or value == ''
    if ret:
        msg = f"{value}" if value else 'empty string'
        ui.notify(f'{label} is invalid. Got {msg}')
    return ret


def is_int_positive(label: str, value: int) -> bool:
    try:
        value = float(value)
    except Exception:
        ui.notify(f'{label} is invalid. Got "{str(value)}"')
        return False

    if value > 0:
        ui.notify(f'{label} is invalid. Got {value}')
        return False

    return True
