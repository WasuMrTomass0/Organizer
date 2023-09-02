from nicegui import ui


class DialogConfirmChoice:

    def __init__(
            self,
            handler_button_confirm,
            handler_button_close = None,
            def_title: str = None,
            def_btn_color_confirm: str = 'red',
            def_btn_color_cancel: str = 'primary',
            def_btn_text_confirm: str = 'Confirm',
            def_btn_text_cancel: str = 'Cancel',
            ) -> None:
        # Defaults
        self.def_title = def_title
        self.def_btn_color_confirm = def_btn_color_confirm
        self.def_btn_color_cancel = def_btn_color_cancel
        self.def_btn_text_confirm = def_btn_text_confirm
        self.def_btn_text_cancel = def_btn_text_cancel
        # Widgets
        self.dlg = None  # type: ui.dialog
        self.crd = None  # type: ui.card
        self.row_1 = None  # type: ui.row
        self.lbl = None  # type: ui.label
        self.btn_confirm = None  # type: ui.button
        self.btn_cancel = None  # type: ui.button
        # Create widgets
        self._create_widget(
            handler_button_confirm=handler_button_confirm,
            handler_button_close=handler_button_close,
        )
        pass

    def _create_widget(
            self,
            handler_button_confirm,
            handler_button_close,
            ) -> None:
        # Default close action is appended to handler
        if handler_button_close is None:
            handler_button_close = self.close
        else:
            def new_fn():
                handler_button_close()
                self.close()
            handler_button_close = new_fn

        # Create objects that are containers for other
        self.dlg = ui.dialog(value=False)
        self.dlg.classes('w-full no-wrap items-center')
        with self.dlg, ui.card().classes('w-full no-wrap items-center') as self.crd:
            # Main text
            self.lbl = ui.label(text=self.def_title)
            # Buttons
            self.row_1 = ui.row()
            self.row_1.classes('w-full no-wrap items-center')
            with ui.row().classes('w-full no-wrap items-center'):
                # Canncel button
                self.btn_cancel = ui.button(
                    text=self.def_btn_text_cancel, 
                    color=self.def_btn_color_cancel,
                    on_click=handler_button_close
                )
                self.btn_cancel.classes('w-1/2')
                # Confirm button
                self.btn_confirm = ui.button(
                    text=self.def_btn_text_confirm, 
                    color=self.def_btn_color_confirm,
                    on_click=handler_button_confirm,
                )
                self.btn_confirm.classes('w-1/2')

    def open(self, title: str = None) -> None:
        if title:
            self.set_text_title(title=title)
        self.dlg.open()

    def close(self) -> None:
        self.dlg.close()

    def set_text_title(self, text: str) -> None:
        self.lbl.set_text(text=text)

    def set_text_btn_confirm(self, text: str) -> None:
        self.btn_confirm.set_text(text=text)

    def set_text_btn_cancel(self, text: str) -> None:
        self.btn_cancel.set_text(text=text)
    
    async def await_choice(self) -> bool:
        choice = await self.dlg
        return choice
