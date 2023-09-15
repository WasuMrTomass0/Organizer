from database.database import Database
from database.locations import Location
from database.container import Container
from database.stored_item import StoredItem
from database.item_in_use import ItemInUse


class Organizer:

    def __init__(
            self,
            username: str = None,
            password: str = None,
            host: str = None,
            port: int = None,
            database: str = None,
        ) -> None:
        self._db = Database(
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )
        self.check_tables()

    def _insert(self, obj) -> None:
        with self._db:
            self._db.insert(obj)

    def _update(self, obj) -> None:
        with self._db:
            self._db.update(obj)

    @staticmethod
    def from_json(path: str) -> "Organizer":
        # Load data
        with open(path, 'r') as f:
            # data = f.read()
            import json
            data = json.load(f)
        # Create object
        return Organizer(
            username=data['username'],
            password=data['password'],
            host=data['host'],
            port=data['port'],
            database=data['database'],
        )

    # COMMON
    def check_tables(self) -> None:
        classes = [Location, Container, StoredItem, ItemInUse]
        for c in classes:
            if self._db.is_table(c):
                continue
            self._db.create_table(cls=c)

    # LOCATIONS
    def add_location(
            self,
            name: str = None,
        ) -> None:
        loc = Location()
        loc.name = name
        self._insert(loc)

    def remove_location(self, name: str) -> None:
        self._db.remove(
            cls=Location,
            conditions=[Location.name == name]
        )

    def get_locations(self) -> "list[Location]":
        with self._db:
            return self._db.get(Location)

    def get_location_names(self) -> "list[str]":
        return sorted([str(d) for d in self.get_locations()])

    def get_locations_grid(self) -> dict:
        return {
            'columnDefs': [
                {'headerName': 'Name', 'field': 'name'},
            ],
            'rowData': [
                {'name': loc.name} for loc in self.get_locations()
            ]
        }

    # CONTAINERS
    def add_container(
            self,
            location: str = None,
            description: str = None,
        ) -> None:
        c = Container()
        c.location = location
        c.description = description
        self._insert(c)

    def remove_container(self, id: int) -> None:
        self._db.remove(
            cls=Container,
            conditions=[Container.id == id]
        )

    def get_containers(self, limit: int = None, conditions: list = None) -> "list[Container]":
        with self._db:
            return self._db.get(Container, limit=limit, conditions=conditions)

    def get_container(self, id: int) -> "Container":
        conditions = [ Container.id == id ]
        return self.get_containers(None, conditions)[0]

    def get_containers_select(self) -> "dict[int, str]":
        """Returns dict made of containers for select.
        {containerid: name, ...}

        Returns:
            dict[int, str]: nicegui's select's input
        """
        def limit(s: str) -> str:
            length = 50
            s = s.replace('\n', '; ')
            return (s[:length]+'...') if len(s) > length else s
        return {
            c.id: f'{c.id}: {limit(c.description)}' for c in self.get_containers()
        }


    def get_containers_grid(self) -> dict:
        return {
            'columnDefs': [
                {'headerName': 'ID', 'field': 'id'},
                {'headerName': 'Location', 'field': 'location', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
                {'headerName': 'Description', 'field': 'description', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
            ],
            'rowData': [
                {
                    'id': c.id,
                    'location': c.location,
                    'description': c.description
                } for c in self.get_containers()
            ]
        }

    # STORED ITEMS
    def add_stored_item(
            self,
            containerid: str,
            name: str,
            description: str,
            quantity: int,
            image: bytes
        ) -> None:
        si = StoredItem()
        si.containerid = int(containerid)
        si.name = name
        si.description = description
        si.quantity = quantity
        si.image = image
        self._insert(si)

    def update_stored_item(
            self,
            id: int,
            containerid: str,
            name: str,
            description: str,
            quantity: int,
            image: bytes
        ) -> None:
        si = self.get_stored_item(id=id)
        si.containerid = int(containerid)
        si.name = name
        si.description = description
        si.quantity = quantity
        si.image = image
        self._insert(si)

    def remove_stored_item(self, id: int) -> None:
        self._db.remove(
            cls=StoredItem,
            conditions=[StoredItem.id == id]
        )

    def get_stored_item(self, id: int) -> StoredItem:
        conditions = [ StoredItem.id == id ]
        return self.get_stored_items(None, conditions)[0]

    def get_stored_items(self, limit: int = None, conditions: list = None) -> "list[StoredItem]":
        with self._db:
            return self._db.get(StoredItem, limit, conditions)

    def get_stored_items_in_container(self, containerid: id) -> "list[StoredItem]":
        conditions = [StoredItem.containerid == containerid]
        return self.get_stored_items(conditions=conditions)

    def get_stored_items_grid(self, name: str = None, containerids: "list[int]" = None) -> dict:
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_filter_operators.htm
        conditions = []
        if name:
            conditions.append(StoredItem.name.like('%' + name + '%'))
        if containerids:
            conditions.append(StoredItem.containerid.in_(containerids))

        data = self.get_stored_items(None, conditions)  # type: list[StoredItem]

        return {
            'columnDefs': [
                {'headerName': 'Stored item', 'field': 'str', 'resizable': True},
                {'headerName': 'Description', 'field': 'description', 'resizable': True}, #'filter': 'agTextColumnFilter', 'floatingFilter': True},
            ],
            'rowData': [
                {
                    'id': si.id,
                    'str': si.name,
                    'description': f'[#{si.quantity}] {si.description}',
                } for si in data
            ]
        }

    # ITEMS IN USE
    def add_item_in_use(self, id: int) -> None:
        # Read item from id
        item = self.get_stored_item(id=id)
        # Create ItemInUse object
        item_in_use = ItemInUse.from_stored_item(item)
        # Add item to in use table
        self._insert(obj=item_in_use)
        # Delete item from storage table
        self.remove_stored_item(item.id)

    def move_item_in_use_back(self, id: int) -> None:
        # Read item from id
        item_in_use = self.get_item_in_use(id=id)
        # Create StoredItem object
        stored_item = ItemInUse.to_stored_item(item_in_use)
        # Add item to stored table
        self._insert(obj=stored_item)
        # Delete item from in use table
        self.remove_item_in_use(item_in_use.id)

    def remove_item_in_use(self, id: int) -> None:
        self._db.remove(
            cls=ItemInUse,
            conditions=[ItemInUse.id == id]
        )

    def get_items_in_use(self, limit: int = None, conditions: list = None) -> "list[StoredItem]":
        with self._db:
            return self._db.get(ItemInUse, limit, conditions)

    def get_item_in_use(self, id: int) -> ItemInUse:
        conditions = [ ItemInUse.id == id ]
        return self.get_items_in_use(None, conditions)[0]

    def get_items_in_use_grid(self, name: str = None, containerids: "list[int]" = None) -> dict:
        conditions = []
        if name:
            conditions.append(ItemInUse.name.like('%' + name + '%'))
        if containerids:
            conditions.append(ItemInUse.containerid.in_(containerids))

        data = self.get_items_in_use(None, conditions)  # type: list[ItemInUse]

        return {
            'columnDefs': [
                {'headerName': 'Stored item', 'field': 'str', 'resizable': True},
                {'headerName': 'Description', 'field': 'description', 'resizable': True}, #'filter': 'agTextColumnFilter', 'floatingFilter': True},
            ],
            'rowData': [
                {
                    'id': si.id,
                    'str': si.name,
                    'description': f'[#{si.quantity}] {si.description}',
                } for si in data
            ]
        }

    pass
