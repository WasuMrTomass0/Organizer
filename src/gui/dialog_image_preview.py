from nicegui import ui
from config import FILE_IMAGE_DEFAULT

from language.language import lang


class DialogImagePreview:

    def __init__(
            self,
            default_image_path: str = FILE_IMAGE_DEFAULT
            ) -> None:
        # Defaults
        self.default_image_path = default_image_path
        # Widgets
        self.dlg = None  # type: ui.dialog
        self.crd = None  # type: ui.card
        self.lbl = None  # type: ui.label
        self.img = None  # type: ui.image
        self.btn = None  # type: ui.button
        # Create widgets
        self._create_widget()
        pass

    def _create_widget(self) -> None:
        # Create objects that are containers for other
        self.dlg = ui.dialog(value=False)
        self.dlg.classes('w-full no-wrap items-center')

        with self.dlg, ui.card().classes('w-full no-wrap items-center') as self.crd:
            self.lbl = ui.label(text='Image preview')
            self.img = ui.image(self.default_image_path)
            self.btn = ui.button(lang.Close, on_click=self.close)
            self.btn.classes('w-full')
        pass

    def open(self) -> None:
        self.dlg.open()

    def close(self) -> None:
        self.dlg.close()

    def set_image_source(self, source) -> None:
        self.img.set_source(source=source)

    def set_title(self, text) -> None:
        self.lbl.set_text(text=text)
