from nicegui import ui

from language.language import lang
from app.organizer import Organizer
from gui.front_data import FrontData


class QuickStatistics:

    def __init__(
            self,
            app: Organizer,
            fdata: FrontData,
            parent,
            classes_width: str,
        ) -> None:
        self._parent = parent
        self._app = app
        self._fdata = fdata
        self._classes_width = classes_width
        self._num_widgets = 4
        self._quick_stats = None  # type: dict
        # Widgets
        self.card = None  # type: ui.card
        self._labels_str = []  # type: list[ui.label]
        self._labels_int = []  # type: list[ui.label]
        # Load widgets
        self._create_widget()

    def __enter__(self):
        self.card.__enter__()

    def __exit__(self):
        self.card.__exit__()

    def _create_widget(self) -> None:
        # Update statistics
        self._load_data()
        self._num_widgets = len(self._quick_stats)
        # Clear list of widgets
        self._labels_str.clear()
        self._labels_int.clear()
        # UI
        with self._parent:
            # Main card
            self.card = ui.card()
            self.card.classes(f'{self._classes_width} no-wrap items-center')
            with self.card:
                # Title
                title = ui.label(lang.Summary)
                title.style('font-size: 150%')
                # Statistics
                with ui.row().classes('w-full items-center justify-between'):
                    # Create widgets
                    for _ in range(self._num_widgets):
                        with ui.card().classes('w-48 items-center'):
                            with ui.column().classes('w-full items-center'):
                                lbl_str = ui.label('')
                                lbl_int = ui.label('').style('font-size: 250%')
                        # Add widgets to list
                        self._labels_str.append(lbl_str)
                        self._labels_int.append(lbl_int)
        # Load data
        self._update_widgets()

    def _load_data(self) -> None:
        self._quick_stats = self._app.get_quick_statistics()

    def _update_widgets(self) -> None:
        for i, (text, integer) in enumerate(self._quick_stats.items()):
            self._labels_str[i].set_text(text)
            self._labels_int[i].set_text(integer)
