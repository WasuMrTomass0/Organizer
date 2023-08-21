import logging

from database.database import Database
from database.locations import Location
from database.container import Container
from database.stored_item import StoredItem


logger = logging.getLogger(__name__)


class Organizer:

    def __init__(
            self,
        ) -> None:
        self._db = Database()
        pass

    def _insert(self, obj) -> None:
        with self._db:
            self._db.insert(obj)

    # LOCATIONS
    def add_location(
            self,
            name: str = None,
        ) -> int:
        loc = Location()
        loc.name = name
        self._insert(loc)
        return 0

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
        ) -> int:
        c = Container()
        c.location = location
        c.description = description
        self._insert(c)
        return 0

    def get_containers(self) -> "list[Container]":
        with self._db:
            return self._db.get(Container)
    
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
            image: bytes
    ) -> None:
        si = StoredItem()
        si.containerid = int(containerid)
        si.name = name
        si.description = description
        si.description = description
        si.image = image
        self._insert(si)
        return 0

    pass
