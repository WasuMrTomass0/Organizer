from nicegui import ui

from language.language import lang


class DialogContainer:

    def __init__(
            self,
            handler_button_delete,
            handler_button_close = None,
            def_btn_color_delete: str = 'red',
            def_btn_color_close: str = 'primary',
            def_btn_text_delete: str = lang.Delete,
            def_btn_text_close: str = lang.Close,
            ) -> None:
        # Defaults
        self.def_btn_color_delete = def_btn_color_delete
        self.def_btn_color_close = def_btn_color_close
        self.def_btn_text_delete = def_btn_text_delete
        self.def_btn_text_close = def_btn_text_close
        # Widgets
        self.dlg = None  # type: ui.dialog
        self.crd = None  # type: ui.card
        self.row_1 = None  # type: ui.row
        self.lbl_title = None  # type: ui.label
        self.lbl_location = None  # type: ui.label
        self.lbl_description = None  # type: ui.label
        self.lbl_items = None  # type: ui.label
        self.btn_delete = None  # type: ui.button
        self.btn_close = None  # type: ui.button
        # Create widgets
        self._create_widget(
            handler_button_delete=handler_button_delete,
            handler_button_close=handler_button_close,
        )
        pass

    def __enter__(self):
        self.open()

    def __exit__(self):
        self.close()

    def append_close_to_handler(self, handler):
        def fn():
            handler()
            self.dlg.close()
        return fn if handler is not None else self.dlg.close

    def _create_widget(
            self,
            handler_button_delete,
            handler_button_close,
            ) -> None:
        # Create objects that are containers for other
        self.dlg = ui.dialog(value=False)
        self.dlg.classes('w-full no-wrap items-center')
        with self.dlg, ui.card().classes('w-full no-wrap') as self.crd:
            # Main text
            self.lbl_title = ui.label(text='lbl_title')
            self.lbl_title.classes('items-center')
            self.lbl_location = ui.label(text='lbl_location')
            self.lbl_description = ui.label(text='lbl_description')
            self.lbl_items = ui.label(text='lbl_items')
            # Buttons
            self.row_1 = ui.row()
            self.row_1.classes('w-full no-wrap items-center')
            with ui.row().classes('w-full no-wrap items-center'):
                # Update handlers
                handler_button_delete = self.append_close_to_handler(handler_button_delete)
                handler_button_close = self.append_close_to_handler(handler_button_close)
                # Cancel button
                self.btn_close = ui.button(
                    text=self.def_btn_text_close,
                    color=self.def_btn_color_close,
                    on_click=handler_button_close
                )
                self.btn_close.classes('w-1/2')
                # Delete button
                self.btn_delete = ui.button(
                    text=self.def_btn_text_delete,
                    color=self.def_btn_color_delete,
                    on_click=handler_button_delete,
                )
                self.btn_delete.classes('w-1/2')

    def open(self) -> None:
        self.dlg.open()

    def close(self) -> None:
        self.dlg.close()

    def load_item(self, item, organizer) -> None:
        # Update UI
        self.lbl_title.set_text(f'{lang.ID}: {str(item.id)}')
        self.lbl_location.set_text(f'{lang.Location}: {str(item.location)}')
        self.lbl_description.set_text(f'{lang.Description}: {str(item.description)}')
        # TODO: Load items for that container - represent as table
        stored_items = organizer.get_stored_items_in_container(containerid=item.id)
        count = len(stored_items)
        self.lbl_items.set_text(f'{lang.Items_in_container}: {str(count)}')

    async def await_choice(self) -> bool:
        choice = await self.dlg
        return choice
