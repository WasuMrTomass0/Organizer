from nicegui import ui
from nicegui import events

from app.organizer import Organizer
from gui.front_data import FrontData
from gui import common as cmn
from gui.dialog_stored_item import DialogStoredItem
from gui.dialog_confirm_choice import DialogConfirmChoice
from gui.dialog_container import DialogContainer
from gui.dialog_image_preview import DialogImagePreview
from gui.card_quick_statistics import QuickStatistics
from logger import debug, info, warning, error, critical
from config import FILE_IMAGE_LOGO, FILE_SECRETS, FILE_IMAGE_FLAG_PL
from config import FILE_IMAGE_FLAG_ENG
from language.language import lang


# Global variables
app = Organizer.from_json(FILE_SECRETS)
fdata = FrontData()
fdata.set('dark_mode', False)

MAX_WIDTH = 1650  # pixels
MIN_WIDTH = 250  # pixels


# Header with links to all pages
def header():
    # Create header with menu and dark/light mode
    header = ui.header(elevated=True, fixed=False)
    header.style('background-color: #3874c8')
    header.classes('items-center justify-between')

    def handler_settings(fn):
        if fn:
            fn()
            ui.notify(lang.Refresh_page_to_see_changes)

    def handler_theme():
        fdata.set('dark_mode', not bool(fdata.get('dark_mode')))

    with header:
        # Menu with pages
        with ui.button(icon='menu'):
            with ui.menu() as menu:
                ui.menu_item(lang.Home_page, lambda: ui.open(page_home))
                ui.separator()
                ui.menu_item(lang.Locations, lambda: ui.open(page_locations))
                ui.menu_item(lang.Containers, lambda: ui.open(page_containers))
                ui.menu_item(f'{lang.Stored_items} - {lang.Create}', lambda: ui.open(page_stored_items_create))
                ui.menu_item(f'{lang.Stored_items} - {lang.Search}', lambda: ui.open(page_stored_items_search))
                ui.menu_item(f'{lang.Stored_items} - {lang.In_use}', lambda: ui.open(page_items_in_use))
        # Title
        with ui.link(target=page_home):
            ui.image(FILE_IMAGE_LOGO).classes('w-40')

        # Dark/Light mode
        dark = ui.dark_mode(value=fdata.get('dark_mode'))
        # Settings
        with ui.button(icon='settings'):
            with ui.menu().classes('w-20') as menu:
                with ui.menu_item(None, lambda: handler_settings(fn=handler_theme)):
                    ui.icon(name='dark_mode').classes('w-full')
                ui.separator()
                with ui.menu_item(None, lambda: handler_settings(fn=lang.set_english)):
                    ui.image(source=FILE_IMAGE_FLAG_ENG)
                with ui.menu_item(None, lambda: handler_settings(fn=lang.set_polish)):
                    ui.image(source=FILE_IMAGE_FLAG_PL)
    pass


@ui.page('/home')
def page_home():
    header()

    def_width = 'w-1/2'

    with ui.column().classes('w-full items-center') as parent:
        card_create = ui.card()
        card_create.classes(f'{def_width} items-center')
        card_create.style(f"max-width:{MAX_WIDTH}px; min-width:{MIN_WIDTH}px;")
        with card_create:
            ui.button(lang.Create_new_item, on_click=lambda: ui.open(page_stored_items_create)).classes('w-full')
            ui.button(lang.Search_for_item, on_click=lambda: ui.open(page_stored_items_search)).classes('w-full')
            ui.button(lang.Items_in_use, on_click=lambda: ui.open(page_items_in_use)).classes('w-full')
            ui.button(lang.Containers, on_click=lambda: ui.open(page_containers)).classes('w-full')
            ui.button(lang.Locations, on_click=lambda: ui.open(page_locations)).classes('w-full')

        card_statistics = QuickStatistics(
            app=app,
            fdata=fdata,
            parent=parent,
            classes_width=def_width,
        )


@ui.page('/locations')
def page_locations():
    # Clear data on entry
    fdata.clear_keys([
        'location_name',
        'selected_location_name',
    ])

    # #Handlers
    @cmn.wrapper_catch_error
    def handler_create_location():
        # Read and check data
        name = fdata.get('location_name')
        if cmn.is_str_empty(lang.Name, name):
            return
        # Process request
        app.add_location(name=name)
        ui.open(page_locations)

    @cmn.wrapper_catch_error
    def handler_confirm():
        name = fdata.get('selected_location_name')
        if name is None:
            ui.notify(f'{lang.Select} {lang.Location} {lang._to_delete}')
            return
        dialog_delete_back.open()

    @cmn.wrapper_catch_error
    def handler_delete():
        name = fdata.get('selected_location_name')
        app.remove_location(name)
        ui.open(page_locations)

    # UI layout
    header()
    with ui.column().classes('w-full items-center'):
        # Dialog - yes no
        dialog_delete_back = DialogConfirmChoice(
            handler_button_confirm=handler_delete,
            def_title=f'{lang.Are_you_sure_you_want_to_delete_} {lang.Location.lower()}?',
            def_btn_text_confirm=lang.Delete,
        )

        # Create new location
        card_create = ui.card()
        card_create.classes('w-full items-center')
        card_create.style(f"max-width:{MAX_WIDTH}px; min-width:{MIN_WIDTH}px;")
        with card_create:
            # Title
            obj = ui.label(f'{lang.Create} {lang.Location.lower()}')
            # Locations name
            inp_name = ui.input(
                label='Name',
                on_change=lambda e: fdata.set('location_name', e.value)
            )
            inp_name.classes('w-full')
            # Main button
            btn_create = ui.button(lang.Create, on_click=handler_create_location)
            btn_create.classes('w-full')

        # List all locations
        card_list = ui.card()
        card_list.classes('w-full items-center')
        card_list.style(f"max-width:{MAX_WIDTH}px; min-width:{MIN_WIDTH}px;")
        with card_list:
            # Title
            obj = ui.label(f'{lang.Existing_} {lang.Locations.lower()} {len(app.get_location_names())}')
            # Locations name
            grid = ui.aggrid(
                options=app.get_locations_grid()
            )
            grid.classes('w-full')
            grid.on('cellClicked', lambda event: fdata.set('selected_location_name', event.args["data"]["name"]))
            # Main button
            btn_create = ui.button(lang.Delete, on_click=handler_confirm)
            btn_create.classes('w-full')


@ui.page('/containers')
def page_containers():
    # Clear data
    fdata.clear_keys([
        'location',
        'description',
        'selected_container_id',
    ])

    # Handlers
    @cmn.wrapper_catch_error
    def handler_create_container():
        # Read data
        loc = fdata.get('location')
        dsc = fdata.get('description')
        # Check data
        if any([cmn.is_str_empty(lang.Description, dsc),
                cmn.is_str_empty(lang.Location, loc),
                ]):
            return
        # Process data
        app.add_container(
            location=loc,
            description=dsc
        )
        ui.open(page_containers)

    @cmn.wrapper_catch_error
    def handler_update_grid():
        grid_data = app.get_containers_grid()['rowData']
        containers_grid.call_api_method('setRowData', grid_data)

    @cmn.wrapper_catch_error
    def handler_show_container(event):
        # Load container and set its id as selected
        container = app.get_container(id=event.args["data"]["id"])
        fdata.set('selected_container_id', container.id)
        # Load and open dialog
        dialog_container.load_item(item=container, organizer=app)
        dialog_container.open()

    @cmn.wrapper_catch_error
    def handler_delete_container():
        # Get containerid to delete
        id = fdata.get('selected_container_id')
        # Check if it is empty
        items = app.get_stored_items_in_container(containerid=id)
        if len(items) != 0:
            ui.notify(f'{lang.Container} {lang._is_not_empty}! {len(items)} {lang._item_s}. ' \
                      f'{lang.Move_them_before_deleting_} {lang.Container.lower()}.')
            dialog_container.open()
            return
        # Process request
        app.remove_container(id)
        handler_update_grid()

    # Page layout
    header()

    with ui.column().classes('w-full items-center'):
        dialog_confirm = DialogConfirmChoice(
            def_title=f'{lang.Are_you_sure_you_want_to_delete_} {lang.Container.lower()}?',
            handler_button_confirm=handler_delete_container,
            def_btn_text_confirm=lang.Delete,
        )
        dialog_container = DialogContainer(
            handler_button_delete=dialog_confirm.open,
        )

        card = ui.card()
        card.classes('w-full items-center')
        card.style(f"max-width:{MAX_WIDTH}px; min-width:{MIN_WIDTH}px;")
        with card:
            obj = ui.label(f'{lang.Create} {lang.Container.lower()}')

            txt = ui.textarea(
                label=lang.Description,
                on_change=lambda e: fdata.set('description', e.value))
            txt.classes('w-full')

            sel_location = ui.select(
                label=lang.Location,
                with_input=True,
                on_change=lambda e: fdata.set('location', e.value),
                options=app.get_location_names())
            sel_location.classes('w-full')

            btn_create = ui.button(lang.Create, on_click=handler_create_container)
            btn_create.classes('w-full')

        # List all containers
        card_list = ui.card()
        card_list.classes('w-full items-center')
        card_list.style(f"max-width:{MAX_WIDTH}px; min-width:{MIN_WIDTH}px;")
        with card_list:
            obj = ui.label(f'{lang.Existing_} {lang.Containers.lower()} {len(app.get_containers())}')

            containers_grid = ui.aggrid(options=app.get_containers_grid())
            containers_grid.on('cellClicked', lambda event: handler_show_container(event))
            containers_grid.classes('w-full')
    pass


@ui.page('/stored_items/create')
def page_stored_items_create(stored_item_id: int = None):
    # Clear data
    fdata.clear_keys([
        'containerid',
        'name',
        'description',
        'image',
    ])
    fdata.set('quantity', 1)

    # Handlers
    @cmn.wrapper_catch_error
    def handler_upload(e: events.UploadEventArguments):
        debug(msg=f'File loaded {e.name = }, {e.type = }, {e.sender = }, {e.client = }, {e.content = }')
        data = e.content.read()
        fdata.set('image', data)

    @cmn.wrapper_catch_error
    def handler_create_stored_item():
        # Read values
        name = fdata.get('name')
        image = fdata.get('image')
        quantity = int(fdata.get('quantity'))
        containerid = fdata.get('containerid')
        description = fdata.get('description')
        # Check data
        if any([
            cmn.is_str_empty(f'{lang.Container} {lang.ID}', containerid),
            cmn.is_str_empty(lang.Name, name),
            not cmn.is_int_positive(lang.Quantity, quantity),
            ]):
            return

        # Process image
        if image:
            image = cmn.process_image(image)
        # Add stored item
        app.add_stored_item(
            containerid=containerid,
            name=name,
            description=description,
            quantity=quantity,
            image=image,
        )
        # Refresh page
        ui.open(page_stored_items_create)

    @cmn.wrapper_catch_error
    def handler_update_stored_item():
        # Read values
        name = fdata.get('name')
        image = fdata.get('image')
        quantity = int(fdata.get('quantity'))
        containerid = fdata.get('containerid')
        description = fdata.get('description')
        # Check data
        if any([
            cmn.is_str_empty(f'{lang.Container} {lang.ID}', containerid),
            cmn.is_str_empty(lang.Name, name),
            not cmn.is_int_positive(lang.Quantity, quantity),
            ]):
            return

        # Process image
        if image:
            image = cmn.process_image(image)
        # Add stored item
        app.update_stored_item(
            id=stored_item_id,
            containerid=containerid,
            name=name,
            description=description,
            quantity=quantity,
            image=image,
        )
        # Go to search
        ui.open(page_stored_items_search)

    # Load stored item's data into widgets
    @cmn.wrapper_catch_error
    def load_data_into_widgets():
        # Get stored item
        item = app.get_stored_item(id=stored_item_id)
        # Update fdata
        fdata.set('name', item.name)
        fdata.set('image', item.image)
        fdata.set('quantity', item.quantity)
        fdata.set('containerid', item.containerid)
        fdata.set('description', item.description)
        # Update UI
        inp_container.set_value(item.containerid)
        inp_name.set_value(item.name)
        txt_desc.set_value(item.description)
        inp_quantity.set_value(item.quantity)
        if item.image:
            dialog_img_prv.set_image_source(cmn.image_to_base64(item.image))

    # Set widgets visible / editable / etc
    def widgets_mode_create():
        col_create.set_visibility(True)
        col_edit.set_visibility(False)

    def widgets_mode_edit():
        col_create.set_visibility(False)
        col_edit.set_visibility(True)

    # Dialog
    dialog_img_prv = DialogImagePreview()

    # UI Layout
    header()

    with ui.column().classes('w-full items-center'):
        card = ui.card()
        card.classes('w-full items-center')
        card.style(f"max-width:{MAX_WIDTH}px; min-width:{MIN_WIDTH}px;")
        with card:
            # Title
            obj = ui.label(f'{lang.Create} {lang.Stored_item.lower()}')
            # Containers
            with ui.row().classes('w-full no-wrap'):
                inp_container = ui.input(
                    label=f'{lang.Container} {lang.ID}',
                    on_change=lambda e: fdata.set('containerid', e.value))
                inp_container.classes('w-1/4')

                sel_location = ui.select(
                    label=lang.Container,
                    with_input=True,
                    on_change=lambda e: fdata.set('containerid', e.value),
                    options=app.get_containers_select())
                sel_location.classes('w-3/4')

                # inp_container.bind_value(sel_location, 'value')
                sel_location.bind_value(inp_container, 'value')
            # Name
            inp_name = ui.input(
                label=lang.Name,
                on_change=lambda e: fdata.set('name', e.value))
            inp_name.classes('w-full')
            # Quantity
            with ui.row().classes('w-full no-wrap'):
                def update_quantity(delta: int) -> None:
                    q = fdata.get('quantity')
                    q = q if q else 0
                    q += delta
                    if q > 0:
                        fdata.set('quantity', q)
                        inp_quantity.set_value(int(q))
                #
                btn_dec = ui.button(icon='remove_circle_outline', on_click=lambda: update_quantity(-1))
                btn_inc = ui.button(icon='add_circle_outline', on_click=lambda: update_quantity(1))
                #
                inp_quantity = ui.number(label=lang.Quantity, value=fdata.get('quantity'),
                on_change=lambda e: fdata.set('quantity', e.value))
                inp_quantity.classes('w-full')
            # Description
            txt_desc = ui.textarea(
                label='Description',
                on_change=lambda e: fdata.set('description', e.value))
            txt_desc.classes('w-full')
            # Image
            upl_img = ui.upload(
                label=f'{lang.Stored_item} {lang.Image}',
                auto_upload=True,
                max_files=1,
                on_upload=lambda e: handler_upload(e))
            upl_img.props('accept=".png,.jpg,.jpeg"')
            upl_img.classes('w-full')

            # Buttons - Create
            with ui.column().classes('w-full no-wrap items-center') as col_create:
                btn_create = ui.button(lang.Create,
                    on_click=handler_create_stored_item)
                btn_create.classes('w-full')
            # Buttons - Edit
            with ui.column().classes('w-full no-wrap items-center') as col_edit:
                btn_img_prv = ui.button(lang.Preview_existing_image, on_click=dialog_img_prv.open)
                btn_img_prv.classes('w-full')
                with ui.row().classes('w-full no-wrap items-center'):
                    btn_close = ui.button(lang.Close, on_click=lambda: ui.open(page_stored_items_search))
                    btn_close.classes('w-1/2')
                    btn_edit = ui.button(lang.Save, on_click=handler_update_stored_item)
                    btn_edit.classes('w-1/2')

    # After creating widgets
    if stored_item_id is not None:
        load_data_into_widgets()
        widgets_mode_edit()
    else:
        widgets_mode_create()


@ui.page('/stored_items/search')
def page_stored_items_search():
    # Clear data
    fdata.clear_keys(keys=[
        'containerids',
        'name',
        'selected_item_id',
    ])

    #  Handlers
    def handler_search():
        grid_data = app.get_stored_items_grid(
            name=fdata.get('name'),
            containerids=fdata.get('containerids'),
        )['rowData']
        sel_stored_items.call_api_method('setRowData', grid_data)

    def handler_show_image(event):
        item = app.get_stored_item(id=event.args["data"]["id"])
        fdata.set('selected_item_id', item.id)
        dialog_item.load_item(item=item)

    # Button handlers
    @cmn.wrapper_catch_error
    def handler_delete():
        app.remove_stored_item(id=fdata.get('selected_item_id'))
        handler_search()
        dialog_item.close()

    @cmn.wrapper_catch_error
    def handler_edit():
        id = fdata.get('selected_item_id')
        if id:
            ui.open(
                target=f'/stored_items/create?stored_item_id={id}',
                new_tab=False
            )

    @cmn.wrapper_catch_error
    def handler_take_out():
        app.add_item_in_use(id=fdata.get('selected_item_id'))
        handler_search()
        dialog_item.close()

    # UI
    header()

    with ui.column().classes('w-full items-center'):
        # Confirm delete dialog
        dialog_choice = DialogConfirmChoice(
            handler_button_close=None,
            handler_button_confirm=handler_delete,
            def_title=f'{lang.Are_you_sure_you_want_to_delete_} {lang.Stored_item.lower()}?',
            def_btn_text_confirm=lang.Delete,
        )
        # Show item dialog
        dialog_item = DialogStoredItem(
            handler_button_delete=dialog_choice.open,
            handler_button_edit=handler_edit,
            handler_button_take_out=handler_take_out,
        )

        # UI layout
        card = ui.card()
        card.classes('w-full items-center')
        card.style(f"max-width:{MAX_WIDTH}px; min-width:{MIN_WIDTH}px;")
        with card:
            # Title
            obj = ui.label(f'{lang.Search_for_} {lang.Stored_item.lower()}')
            # Containers to search in
            sel_location = ui.select(
                label=f'{lang.Container} ({lang.Leave_empty_to_search_in_all})',
                with_input=True,
                multiple=True,
                on_change=lambda e: [fdata.set('containerids', e.value), handler_search()],
                options=app.get_containers_select())
            sel_location.classes('w-full')
            # Name
            inp_name = ui.input(
                label=lang.Name,
                on_change=lambda e: [fdata.set('name', e.value), handler_search()])
            inp_name.classes('w-full')
            # Search results
            sel_stored_items = ui.aggrid(options=app.get_stored_items_grid())
            sel_stored_items.on('cellClicked', lambda event: handler_show_image(event))
            inp_name.classes('w-full')


@ui.page('/stored_items/in-use')
def page_items_in_use():
    # Clear data
    fdata.clear_keys(keys=[
        'containerids',
        'name',
        'selected_item_id',
    ])

    #  Handlers
    def handler_search():
        grid_data = app.get_items_in_use_grid(
            name=fdata.get('name'),
            containerids=fdata.get('containerids'),
        )['rowData']
        sel_stored_items.call_api_method('setRowData', grid_data)

    def handler_show_image(event):
        item = app.get_item_in_use(id=event.args["data"]["id"])
        fdata.set('selected_item_id', item.id)
        dialog_item.load_item(item=item)

    # Button handlers
    @cmn.wrapper_catch_error
    def handler_delete():
        app.remove_item_in_use(id=fdata.get('selected_item_id'))
        handler_search()
        dialog_item.close()

    @cmn.wrapper_catch_error
    def handler_edit():
        ui.notify(lang.Stored_item_can_be_modified_only_from_search_page)

    @cmn.wrapper_catch_error
    def handler_put_back():
        app.move_item_in_use_back(id=fdata.get('selected_item_id'))
        handler_search()
        dialog_item.close()

    # UI
    header()

    with ui.column().classes('w-full items-center'):
        # Confirm delete dialog
        dialog_choice = DialogConfirmChoice(
            handler_button_close=None,
            handler_button_confirm=handler_delete,
            def_title=f'{lang.Are_you_sure_you_want_to_delete_} {lang.Stored_item.lower()}?',
            def_btn_text_confirm=lang.Delete,
        )
        # Show item dialog
        dialog_item = DialogStoredItem(
            handler_button_delete=dialog_choice.open,
            handler_button_edit=handler_edit,
            handler_button_take_out=handler_put_back,
        )
        dialog_item.btn_take_out.set_text(lang.Put_back)

        # UI layout
        card = ui.card()
        card.classes('w-full items-center')
        card.style(f"max-width:{MAX_WIDTH}px; min-width:{MIN_WIDTH}px;")
        with card:
            # Title
            obj = ui.label(f'{lang.Search_for_} {lang.Item_in_use.lower()}')
            # Containers to search in
            sel_location = ui.select(
                label=f'{lang.Previously_assigned_container} ({lang.Leave_empty_to_search_in_all.lower()})',
                with_input=True,
                multiple=True,
                on_change=lambda e: [fdata.set('containerids', e.value), handler_search()],
                options=app.get_containers_select())
            sel_location.classes('w-full')
            # Name
            inp_name = ui.input(
                label=lang.Name,
                on_change=lambda e: [fdata.set('name', e.value), handler_search()])
            inp_name.classes('w-full')
            # Search results
            sel_stored_items = ui.aggrid(options=app.get_items_in_use_grid())
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
