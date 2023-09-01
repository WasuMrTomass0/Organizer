from logging import ERROR

import sqlalchemy
from nicegui import ui
from nicegui import events

from app.organizer import Organizer
from gui.front_data import FrontData
import gui.common as cmn
from logger import log


# Global variables
app = Organizer()
fdata = FrontData()


# Header with links to all pages
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
        with ui.link(target=page_home):
            ui.image('data\organizer_logo.png').classes('w-64')

        # Dark/Light mode
        dark = ui.dark_mode()
        # light_mode dark_mode
        obj = ui.button(icon='light_mode', on_click=lambda: dark.toggle())
        obj.disable()

    pass


@ui.page('/home')
def page_home():
    header()

    with ui.column().classes('w-full items-center'):
        card_create = ui.card()
        card_create.classes('w-full items-center')
        card_create.style("max-width:1000px; min-width:250px;")
        with card_create:
            ui.button('Item Create', on_click=lambda: ui.open(page_stored_items_create)).classes('w-full')
            ui.button('Item Search', on_click=lambda: ui.open(page_stored_items_search)).classes('w-full')
            ui.button('Location', on_click=lambda: ui.open(page_locations)).classes('w-full')
            ui.button('Container', on_click=lambda: ui.open(page_containers)).classes('w-full')


@ui.page('/locations')
def page_locations():
    # Clear data on entry
    fdata.clear('location_name')
    fdata.clear('selected_location_name')

    # # # # # # # #
    def handler_create_location():
        # Read data
        name = fdata.get('location_name')
        # Check data
        if cmn.is_str_empty('Location\'s name', name):
            return
        try:
            app.add_location(
                name=name
            )
        except Exception as err:
            msg = 'Error during creation of location'
            ui.notify(msg)
            log(ERROR, f'{msg} Error: {str(err)}')
        else:
            ui.open(page_locations)

    # # # # # # # #
    async def handler_delete_location():
        dialog_yes_no.open()
        yes = await dialog_yes_no
        if not yes:
            return

        name = fdata.get('selected_location_name')
        if name is None:
            ui.notify(f'Select location to delete')
            return
        try:
            app.remove_location(name)
        except sqlalchemy.exc.IntegrityError as err:
            msg = 'Can\'t remove location that is used by containers'
            ui.notify(msg)
            log(ERROR, f'{msg} Error: {str(err)}')

        except Exception as err:
            msg = 'Error during deletion of location'
            ui.notify(msg)
            log(ERROR, f'{msg} Error: {str(err)}')
        else:
            ui.open(page_locations)

    # # # # # # # # # # # # # # # #
    # Page layout
    header()

    with ui.column().classes('w-full items-center'):
        # Dialog - yes no
        dialog_yes_no = cmn.create_dialog_yes_no(label=None)

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
            grid.on('cellClicked', lambda event: fdata.set('selected_location_name', event.args["data"]["name"]))

            btn_create = ui.button('Delete', on_click=handler_delete_location)
            btn_create.classes('w-full')
    pass


@ui.page('/containers')
def page_containers():
    # Clear data
    fdata.clear('location')
    fdata.clear('description')
    fdata.clear('selected_container_id')

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
            ui.open(page_containers)

    def handler_show_container(event):
        # Load container
        cnt = app.get_container(id=event.args["data"]["id"])
        # Set selected id
        fdata.set('selected_container_id', cnt.id)
        # Update labels
        count = len(app.get_stored_items_in_container(containerid=cnt.id))
        label = f'ID: {str(cnt.id)}, Items: {count}'
        dialog_label_id.set_text(label)
        dialog_label_loc.set_text('Location: ' + str(cnt.location))
        dialog_label_dsc.set_text('Description: ' + str(cnt.description))
        # Show dialog
        dial_show_c.open()

    async def handler_delete_container():
        # Confirm choice
        dialog_yes_no.open()
        yes = await dialog_yes_no
        if not yes:
            return
        # Delete container
        id = fdata.get('selected_container_id')
        if id is None:
            ui.notify(f'Select container to delete')
            return
        try:
            app.remove_container(id)
        except sqlalchemy.exc.IntegrityError as err:
            msg = 'Can\'t remove container that is used by stored items'
            ui.notify(msg)
            log(ERROR, f'{msg} Error: {str(err)}')
        except Exception as err:
            msg = 'Error during deletion of container'
            ui.notify(msg)
            log(ERROR, f'{msg} Error: {str(err)}')
            raise err
        else:
            ui.open(page_containers)
        pass

    # Page layout
    header()

    with ui.column().classes('w-full items-center'):
        # Dialog - yes no
        dialog_yes_no = cmn.create_dialog_yes_no(label=None)

        # Dialog - show container
        dial_show_c = ui.dialog(value=False)
        dial_show_c.classes('w-full')
        with dial_show_c, ui.card().classes('w-full'):
            dialog_label_id = ui.label('Container info:')
            dialog_label_loc = ui.label('Container info:')
            dialog_label_dsc = ui.label('Description')
            #
            with ui.row().classes('w-full no-wrap'):
                dialog_btn_edit = ui.button('Delete', color='red', on_click=handler_delete_container)
                dialog_btn_edit.classes('w-1/2')
                #
                dialog_btn_close = ui.button('Close', on_click=dial_show_c.close)
                dialog_btn_close.classes('w-1/2')

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

            grid = ui.aggrid(options=app.get_containers_grid())
            grid.on('cellClicked', lambda event: handler_show_container(event))
            grid.classes('w-full')
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
            cmn.is_str_empty('Container QR Code', containerid),
            cmn.is_str_empty('Name', name),
            # cmn.is_str_empty('Description', description),
            cmn.is_int_positive('Quantity', quantity),
        ])
        # Image can be None
        # if image is None:
        #     err = True
        #     ui.notify('Upload image')

        if err:
            return

        try:
            if image:
                image = cmn.process_image(image)
        except Exception as err:
            ui.notify('Image error\n\n' + str(err))
            raise err

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


    with ui.column().classes('w-full items-center'):
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
    fdata.clear('selected_item_id')

    def handler_search():
        sel_stored_items.call_api_method(
            'setRowData',
            app.get_stored_items_grid(
                name=fdata.get('name'),
                containerids=fdata.get('containerids'),
            )['rowData']
        )
        pass

    def handler_show_image(event):
        # Load sotred item
        si = app.get_stored_item(id=event.args["data"]["id"])
        # Set selected id
        fdata.set('selected_item_id', si.id)
        # Set dialog widgets
        dialog_label.set_text(
            f'ID{si.id} [#{si.quantity}] {si.name}'
        )
        dialog_label_dsc.set_text(si.description)
        dial_show_si.open()
        # Load image and update image object
        if si.image is not None:
            dialog_image.set_source(cmn.image_to_base64(si.image))
        else:
            with open('data/no_photo.jpg', 'rb') as f:
                dialog_image.set_source(cmn.image_to_base64(f.read()))
        pass

    async def handler_delete():
        dialog_yes_no.open()
        yes = await dialog_yes_no
        if yes:
            try:
                app.remove_stored_item(id=fdata.get('selected_item_id'))
            except Exception as err:
                ui.notify(str(err))
                raise err
            else:
                ui.open(page_stored_items_search)

    def handler_item_take_out():
        try:
            app.add_item_in_use(id=fdata.get('selected_item_id'))
        except Exception as err:
            ui.notify(str(err))
            raise err
        else:
            ui.open(page_stored_items_search)

    header()

    with ui.column().classes('w-full items-center'):
        # Dialog - yes no
        dialog_yes_no = cmn.create_dialog_yes_no(label=None)

        # Dialog - show image
        dial_show_si = ui.dialog(value=False)
        dial_show_si.classes('w-full')
        with dial_show_si, ui.card().classes('w-full'):
            dialog_label = ui.label('Image content:')
            with ui.card().classes('w-full'):
                dialog_label_dsc = ui.label('Description')
            #
            dialog_image = ui.image('data/no_photo.jpg')
            #
            with ui.row().classes('w-full no-wrap'):
                dialog_btn_edit = ui.button('Delete', color='red', on_click=handler_delete)
                dialog_btn_edit.classes('w-1/2')
                #
                dialog_btn_edit = ui.button('Edit')
                dialog_btn_edit.classes('w-1/2')
                dialog_btn_edit.disable()
            #
            with ui.row().classes('w-full no-wrap'):
                dialog_btn_take_out = ui.button('Take out', on_click=handler_item_take_out)
                dialog_btn_take_out.classes('w-1/2')
                #
                dialog_btn_close = ui.button('Close', on_click=dial_show_si.close)
                dialog_btn_close.classes('w-1/2')

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
            sel_stored_items.on('cellClicked', lambda event: handler_show_image(event))
            inp_name.classes('w-full')


def main() -> None:
    header()
    ui.open(page_home)
    ui.run(
        title='Organizer',
        favicon='🚀',
        dark=None,
        viewport='width=device-width, initial-scale=1',
    )
