from nicegui import ui
from contextlib import contextmanager


@contextmanager
def disable_element(element) -> None:
    element.disable()
    try:
        yield
    finally:
        element.enable()
