from nicegui import ui
from nicegui import events
# from PIL import Image
# import io

from app.organizer import Organizer
from gui.front_data import FrontData
from gui.common import is_str_empty, is_int_positive


#
app = Organizer()
fdata = FrontData()


def header():
    # Create header with menu and dark/light mode
    header = ui.header(elevated=True, fixed=False)
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
                ui.menu_item('Stored items - Create', lambda: ui.open(page_stored_items_create))
                ui.menu_item('Stored items - Search', lambda: ui.open(page_stored_items_search))
        # Title
        ui.label('Organizer')
        # Dark/Light mode
        dark = ui.dark_mode()
        # light_mode dark_mode
        obj = ui.button(icon='light_mode', on_click=lambda: dark.toggle())

    pass


@ui.page('/home')
def page_home():
    header()

    card_create = ui.card()
    card_create.classes('w-full items-center')
    card_create.style("max-width:1500px; min-width:250px;")
    with card_create:
        btn_csi = ui.button('Create stored item', on_click=lambda: None)
        btn_csi.classes('w-full')

        btn_ssi = ui.button('Search for stored item', on_click=lambda: None)
        btn_ssi.classes('w-full')


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
        inp_name.classes('w-full')

        btn_create = ui.button('Create', on_click=handler_create_location)
        btn_create.classes('w-full')

    # List all locations
    card_list = ui.card()
    card_list.classes('w-full items-center')
    card_list.style("max-width:1000px; min-width:250px;")
    with card_list:
        obj = ui.label(f'Existing locations {len(app.get_location_names())}')

        grid = ui.aggrid(
            options=app.get_locations_grid()
        )
        grid.classes('w-full')

        btn_create = ui.button('Delete', on_click=handler_delete_location)
        btn_create.classes('w-full')
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
        txt.classes('w-full')

        sel_location = ui.select(
            label='Location',
            with_input=True,
            on_change=lambda e: fdata.set('location', e.value),
            options=app.get_location_names())
        sel_location.classes('w-full')

        btn_create = ui.button('Create', on_click=lambda e: handler_create_container(e.sender))
        btn_create.classes('w-full')

    # List all containers
    card_list = ui.card()
    card_list.classes('w-full items-center')
    card_list.style("max-width:1000px; min-width:250px;")
    with card_list:
        obj = ui.label(f'Existing containers {len(app.get_containers())}')

        grid = ui.aggrid(
            options=app.get_containers_grid()
        )
        grid.classes('w-full')

        btn_create = ui.button('Delete')
        btn_create.classes('w-full')
        btn_create.disable()
    pass


@ui.page('/stored_items/create')
def page_stored_items_create():
    # Clear data
    fdata.clear('containerid')
    fdata.clear('name')
    fdata.clear('description')
    fdata.set('quantity', 1)
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
        quantity = fdata.get('quantity')
        image = fdata.get('image')
        # Check data
        err = any([
            is_str_empty('Container QR Code', containerid),
            is_str_empty('Name', name),
            is_str_empty('Description', description),
            is_int_positive('Quantity', quantity),
        ])
        # Image can be None
        # if image is None:
        #     err = True
        #     ui.notify('Upload image')

        if err:
            return

        try:
            app.add_stored_item(
                containerid=containerid,
                name=name,
                description=description,
                quantity=quantity,
                image=image,
            )
        except Exception as err:
            ui.notify(str(err))
            raise err

        ui.open(page_stored_items_create)

        pass

    header()

    card = ui.card()
    card.classes('w-full items-center')
    card.style("max-width:1000px; min-width:250px;")
    with card:
        # Title
        obj = ui.label('Create stored item')
        # Containers
        with ui.row().classes('w-full no-wrap'):
            inp_container = ui.input(
                label='QR code',
                on_change=lambda e: fdata.set('containerid', e.value))
            inp_container.classes('w-1/4')

            sel_location = ui.select(
                label='Container',
                with_input=True,
                on_change=lambda e: fdata.set('containerid', e.value),
                options=app.get_containers_select())
            sel_location.classes('w-3/4')

            # inp_container.bind_value(sel_location, 'value')
            sel_location.bind_value(inp_container, 'value')
        # Name
        inp_name = ui.input(
            label='Name',
            on_change=lambda e: fdata.set('name', e.value))
        inp_name.classes('w-full')
        # Quantity
        with ui.row().classes('w-full no-wrap'):
            def update_quantity(delta: int) -> None:
                x = fdata.get('quantity') + delta
                if x > 0:
                    fdata.set('quantity', x)
                    inp_quantity.set_value(int(x))
            #
            btn_dec = ui.button(icon='remove_circle_outline', on_click=lambda: update_quantity(-1))
            btn_inc = ui.button(icon='add_circle_outline', on_click=lambda: update_quantity(1))
            #
            inp_quantity = ui.number(label='Quantity', value=fdata.get('quantity'),
            on_change=lambda e: fdata.set('quantity', e.value))
            inp_quantity.classes('w-full')
        # Description
        txt = ui.textarea(
            label='Description',
            on_change=lambda e: fdata.set('description', e.value))
        txt.classes('w-full')
        # Image
        upl_img = ui.upload(
            label='Item image',
            auto_upload=True,
            max_files=1,
            on_upload=handler_upload)
        upl_img.props('accept=".png,.jpg,.jpeg"')
        upl_img.classes('w-full')
        # Creation
        btn_create = ui.button('Create',
            on_click=handler_create_stored_item)
        btn_create.classes('w-full')

    pass


@ui.page('/stored_items/search')
def page_stored_items_search():
    # Clear data
    fdata.clear('containerids')
    fdata.clear('name')

    def handler_search():
        sel_stored_items.call_api_method(
            'setRowData',
            app.get_stored_items_grid(
                name=fdata.get('name'),
                containerids=fdata.get('containerids'),
            )['rowData']
        )
        pass

    header()

    card = ui.card()
    card.classes('w-full items-center')
    card.style("max-width:1000px; min-width:250px;")
    with card:
        # Title
        obj = ui.label('Search for stored item')

        # Containers to search in
        sel_location = ui.select(
            label='Container (leave empty to search in all)',
            with_input=True,
            multiple=True,
            on_change=lambda e: [fdata.set('containerids', e.value), handler_search()],
            options=app.get_containers_select())
        sel_location.classes('w-full')

        # Name
        inp_name = ui.input(
            label='Name',
            on_change=lambda e: [fdata.set('name', e.value), handler_search()])
        inp_name.classes('w-full')

        # Search results
        sel_stored_items = ui.aggrid(options=app.get_stored_items_grid())
        sel_stored_items.on('cellClicked', lambda event: ui.notify(f'Cell value: {event.args["value"]}'))
        inp_name.classes('w-full')
        


def main() -> None:
    header()
    ui.run(
        title='Organizer',
        favicon='🚀',
        dark=None,
        viewport='width=device-width, initial-scale=1',
    )
