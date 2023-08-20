from nicegui import ui
from app.organizer import Organizer
from gui.front_data import FrontData
from gui.common import disable_element

# 
app = Organizer()
fdata = FrontData()

dialog = ui.dialog()


def header():
    # Create header with menu and dark/light mode
    header = ui.header(elevated=True)
    header.style('background-color: #3874c8')
    header.classes('items-center justify-between')

    with header:
        # Menu with pages
        with ui.button(icon='menu'):
            with ui.menu() as menu:
                ui.menu_item('Home', lambda: ui.open(page_home))
                ui.separator()
                ui.menu_item('Container create', lambda: ui.open(page_create_container))
                ui.menu_item('Container list', lambda: ui.open(page_list_container))
        # Title
        ui.label('Organizer')
        # Dark/Light mode
        dark = ui.dark_mode()
        # light_mode dark_mode
        obj = ui.button(icon='light_mode', on_click=lambda: dark.toggle())
    
    with dialog, ui.card():
        ui.label('Processing!')
        ui.spinner(size='lg')
        ui.spinner('audio', size='lg', color='green')
        ui.spinner('dots', size='lg', color='red')
    pass


@ui.page('/home')
def page_home():
    header()

@ui.page('/create_container')
def page_create_container():
    # Temp
    locations = ['Attic', 'Garage']

    # handler_create_container
    def handler_create_container(button: ui.button):
        # Read data
        loc = fdata.get('location')
        dsc = fdata.get('description')

        # Check data
        if dsc is None or dsc == '':
            msg = f"{dsc}" if dsc else 'empty string'
            ui.notify(f'Description is invalid. Got {msg}')
            return
        if loc is None or loc == '':
            msg = f"{loc}" if loc else 'empty string'
            ui.notify(f'Location is invalid. Got {msg}')
            return
        
        # Process data
        code = app.add_container(
            location=loc,
            description=dsc
        )

        # Notify user
        if code:
            ui.notify(f'Error during creation of container')
        else:
            ui.notify(f'Container created')
            # ui.open(page_create_container)

    # Page layout
    header()

    card = ui.card()
    card.classes('w-full items-center')
    card.style("max-width:1000px; min-width:250px;")

    with card:
        obj = ui.label('Create container')

        obj = ui.textarea(
            label='Description', 
            on_change=lambda e: fdata.set('description', e.value))
        obj.classes('w-3/4')
        
        obj = ui.select(
            label='Location', 
            with_input=True, 
            on_change=lambda e: fdata.set('location', e.value), 
            options=locations)
        obj.classes('w-3/4')

        obj = ui.button('Create', on_click=lambda e: handler_create_container(e.sender))
        obj.classes('w-3/4')
    pass


@ui.page('/list_container')
def page_list_container():
    header()

    card = ui.card()
    card.classes('w-full items-center')
    card.style("min-width:250px; max-width:1000px;")

    with card:
        obj = ui.label('List container')

    pass


def main() -> None:
    header()
    ui.run(
        title='Organizer',
        favicon='🚀',
        dark=True,
        viewport='width=device-width, initial-scale=1',
    )
