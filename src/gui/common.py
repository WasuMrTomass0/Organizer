from nicegui import ui
from contextlib import contextmanager
from PIL import Image
import base64
from PIL import Image
from io import BytesIO


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


# Prepare image for storage in database
def process_image(image: bytes, dim: tuple = (1024,1024), preserve_ratio: bool = True) -> bytes:
    # Create Image object from bytes
    img = Image.open(BytesIO(image))
    # Resize image
    if preserve_ratio:
        img.thumbnail(dim)
    else:
        img = img.resize(dim)
    # Convert to RGB format
    img = img.convert("RGB")
    # Convert to JPEG format
    bytes_o = BytesIO()
    img.save(bytes_o, 'jpeg')
    return bytes_o.getvalue()


# max_dim: list = None
def image_to_base64(image: bytes) -> str:
    return f'data:image/jpeg;base64,{base64.b64encode(image).decode("ascii")}'


def create_dialog_yes_no(label: str = None) -> ui.dialog:
    # Question / Sentence displayed
    label = label if label else 'Are you sure?'
    # Widgets
    with ui.dialog(value=False) as dialog, ui.card():
        ui.label(label)
        with ui.row():
            ui.button('Yes', color='red', on_click=lambda: dialog.submit(True))
            ui.button('No', color='green', on_click=lambda: dialog.submit(False))
    return dialog
