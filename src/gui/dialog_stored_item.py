from nicegui import ui

import gui.common as cmn
from config import FILE_IMAGE_DEFAULT

from language.language import lang


class DialogStoredItem:

    def __init__(
            self,
            handler_button_delete,
            handler_button_edit,
            handler_button_take_out,
            default_image_path: str = FILE_IMAGE_DEFAULT
            ) -> None:
        # Defaults
        self.default_image_path = default_image_path
        # Widgets
        self.dlg = None  # type: ui.dialog
        self.crd = None  # type: ui.card
        self.row_1 = None  # type: ui.row
        self.row_2 = None  # type: ui.row
        self.lbl_title = None  # type: ui.label
        self.lbl_desc = None  # type: ui.label
        self.img = None  # type: ui.image
        self.btn_delete = None  # type: ui.button
        self.btn_edit = None  # type: ui.button
        self.btn_take_out = None  # type: ui.button
        self.btn_close = None  # type: ui.button
        # Create widgets
        self._create_widget(
            handler_button_delete=handler_button_delete,
            handler_button_edit=handler_button_edit,
            handler_button_take_out=handler_button_take_out,
        )
        pass

    def _create_widget(
            self,
            handler_button_delete,
            handler_button_edit,
            handler_button_take_out,
            ) -> None:
        # Create objects that are containers for other
        self.dlg = ui.dialog(value=False)
        self.dlg.classes('w-full no-wrap items-center')

        with self.dlg, ui.card().classes('w-full no-wrap items-center') as self.crd:
            self.lbl_title = ui.label(text='Title - Default text')
            self.lbl_desc = ui.label(text='Description - Default text')
            self.lbl_desc.classes('w-full')
            self.img = ui.image(self.default_image_path)
            #
            self.col_1 = ui.column()
            self.col_1.classes('w-full no-wrap items-center')
            self.row_1 = ui.row()
            self.row_1.classes('w-full no-wrap items-center')
            with ui.row().classes('w-full no-wrap items-center'):
                # Delete
                self.btn_delete = ui.button(lang.Delete, color='red', on_click=handler_button_delete)
                self.btn_delete.classes('w-1/2')
                # Edit
                self.btn_edit = ui.button(lang.Edit, on_click=handler_button_edit)
                self.btn_edit.classes('w-1/2')
            #
            self.row_2 = ui.row()
            self.row_2.classes('w-full no-wrap items-center')
            with self.row_2:
                # Take out
                self.btn_take_out = ui.button(lang.Take_out, on_click=handler_button_take_out)
                self.btn_take_out.classes('w-1/2')
                # Close
                self.btn_close = ui.button(lang.Close, on_click=self.dlg.close)
                self.btn_close.classes('w-1/2')
        pass

    def open(self) -> None:
        self.dlg.open()

    def close(self) -> None:
        self.dlg.close()

    def set_image_source(self, source) -> None:
        self.img.set_source(source=source)

    def set_title(self, text) -> None:
        self.lbl_title.set_text(text=text)

    def set_description(self, text) -> None:
        self.lbl_desc.set_text(text=text)

    def load_item(self, item) -> None:
        # Set labels
        self.set_title(f'ID-{item.id} [#{item.quantity}] {item.name}')
        self.set_description(item.description)
        # Set image source
        if item.image is not None:
            source = item.image
        else:
            with open(self.default_image_path, 'rb') as f:
                source = f.read()
        # Set image
        self.set_image_source(cmn.image_to_base64(source))
        # Open dialog
        self.open()
