import logging

from database.database import Database
from database.container import Container
from database.stored_item import StoredItem


logger = logging.getLogger(__name__)


class Organizer:

    def __init__(
            self,
        ) -> None:
        self._db = Database()
        pass

    def add_container(
            self,
            location: str = None,
            description: str = None,
        ) -> int:
        c = Container()
        c.location = location
        c.description = description
        self._db.insert(c)
        return 0

    pass
