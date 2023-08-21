from nicegui import ui
from nicegui import events
# from PIL import Image
# import io

from app.organizer import Organizer
from gui.front_data import FrontData
from gui.common import is_str_empty


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
                ui.menu_item('Locations', lambda: ui.open(page_locations))
                ui.menu_item('Containers', lambda: ui.open(page_containers))
                ui.menu_item('Stored items', lambda: ui.open(page_stored_items))
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


@ui.page('/locations')
def page_locations():
    # # # # # # # # 
    def handler_create_location():
        # Read data
        name = fdata.get('location_name')
        # Check data
        if name is None or name == '':
            msg = f"{name}" if name else 'empty string'
            ui.notify(f'Name is invalid. Got {msg}')
            return
        # Process data
        code = app.add_location(
            name=name
        )
        # Notify user
        if code:
            ui.notify(f'Error during creation of location')
        else:
            fdata.clear('location_name')
            ui.open(page_locations)

    # # # # # # # # 
    def handler_delete_location():
        pass

    # # # # # # # # # # # # # # # # 
    # Page layout
    header()

    # Create new location
    card_create = ui.card()
    card_create.classes('w-full items-center')
    card_create.style("max-width:1000px; min-width:250px;")
    with card_create:
        obj = ui.label('Create location')

        inp_name = ui.input(
            label='Name',
            on_change=lambda e: fdata.set('location_name', e.value)
        )
        inp_name.classes('w-3/4')

        btn_create = ui.button('Create', on_click=handler_create_location)
        btn_create.classes('w-3/4')
    
    # List all locations
    card_list = ui.card()
    card_list.classes('w-full items-center')
    card_list.style("max-width:1000px; min-width:250px;")
    with card_list:
        obj = ui.label(f'Existing locations {len(app.get_location_names())}')

        grid = ui.aggrid(
            options=app.get_locations_grid()
        )
        grid.classes('w-3/4')

        btn_create = ui.button('Delete', on_click=handler_delete_location)
        btn_create.classes('w-3/4')
        btn_create.disable()
    pass


@ui.page('/containers')
def page_containers():
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
            fdata.clear('location')
            fdata.clear('description')
            ui.open(page_containers)

    # Page layout
    header()

    card = ui.card()
    card.classes('w-full items-center')
    card.style("max-width:1000px; min-width:250px;")
    with card:
        obj = ui.label('Create container')

        txt = ui.textarea(
            label='Description',
            on_change=lambda e: fdata.set('description', e.value))
        txt.classes('w-3/4')

        sel_location = ui.select(
            label='Location',
            with_input=True,
            on_change=lambda e: fdata.set('location', e.value),
            options=app.get_location_names())
        sel_location.classes('w-3/4')

        btn_create = ui.button('Create', on_click=lambda e: handler_create_container(e.sender))
        btn_create.classes('w-3/4')
    
    # List all containers
    card_list = ui.card()
    card_list.classes('w-full items-center')
    card_list.style("max-width:1000px; min-width:250px;")
    with card_list:
        obj = ui.label(f'Existing containers {len(app.get_containers())}')

        grid = ui.aggrid(
            options=app.get_containers_grid()
        )
        grid.classes('w-3/4')

        btn_create = ui.button('Delete')
        btn_create.classes('w-3/4')
        btn_create.disable()
    pass


@ui.page('/stored_items')
def page_stored_items():
    # Clear data
    fdata.clear('containerid')
    fdata.clear('name')
    fdata.clear('description')
    fdata.clear('image')

    def handler_upload(e: events.UploadEventArguments):
        # ui.notify(f'{e.name = }, {e.type = }, {e.sender = }, {e.client = }, {e.content = }'        )
        data = e.content.read()
        fdata.set('image', data)

    def handler_create_stored_item():
        # Read values
        containerid = fdata.get('containerid')
        name = fdata.get('name')
        description = fdata.get('description')
        image = fdata.get('image')
        # Check data
        err = any([
            is_str_empty('Container QR Code', containerid),
            is_str_empty('Name', name),
            is_str_empty('Description', description),
        ])
        if image is None:
            err = True
            ui.notify('Upload image')

        if err:
            return

        app.add_stored_item(
            containerid=containerid,
            name=name,
            description=description,
            image=image,
        )  
        
        pass

    header()

    card = ui.card()
    card.classes('w-full items-center')
    card.style("max-width:1000px; min-width:250px;")
    with card:
        obj = ui.label('Create stored item')

        inp_container = ui.input(
            label='Container QR code',
            on_change=lambda e: fdata.set('containerid', e.value))
        inp_container.classes('w-3/4')

        inp_name = ui.input(
            label='Name',
            on_change=lambda e: fdata.set('name', e.value))
        inp_name.classes('w-3/4')

        txt = ui.textarea(
            label='Description',
            on_change=lambda e: fdata.set('description', e.value))
        txt.classes('w-3/4')

        # sel_location = ui.select(
        #     label='Location',
        #     with_input=True,
        #     on_change=lambda e: fdata.set('location', e.value),
        #     options=app.get_location_names())
        # sel_location.classes('w-3/4')

        upl_img = ui.upload(
            label='Item image',
            auto_upload=True,
            max_files=1,
            on_upload=handler_upload)
        upl_img.props('accept=".png,.jpg,.jpeg"')
        upl_img.classes('w-3/4')

        btn_create = ui.button('Create', 
            on_click=handler_create_stored_item)
        btn_create.classes('w-3/4')

    pass


def main() -> None:
    header()
    ui.run(
        title='Organizer',
        favicon='🚀',
        dark=True,
        viewport='width=device-width, initial-scale=1',
    )
