from nicegui import ui
from contextlib import contextmanager
from PIL import Image
import base64
from PIL import Image
from io import BytesIO
from logger import error

from language.language import lang


def wrapper_catch_error(fn):
    def new_fn(*args, **kwargs):
        try:
            ret = fn(*args, **kwargs)
        except Exception as err:
            ui.notify(f'Error occured: {str(err)}')
            error(msg=str(err), delta=1)
            raise err
        else:
            return ret
    return new_fn


def is_str_empty(label: str, value: str) -> bool:
    ret = value is None or value == ''
    if ret:
        msg = str(value) if value else lang.empty_string
        ui.notify(f'{label} {lang.is_invalid}. {lang.Got} {msg}')
    return ret


def is_int_positive(label: str, value: int) -> bool:
    try:
        value = float(value)
    except Exception:
        ui.notify(f'{label} {lang.is_invalid}. {lang.Got} "{str(value)}"')
        return False

    if value <= 0:
        ui.notify(f'{label} {lang.is_invalid}. {lang.Got} {value}')
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


def image_to_base64(image: bytes) -> str:
    return f'data:image/jpeg;base64,{base64.b64encode(image).decode("ascii")}'
