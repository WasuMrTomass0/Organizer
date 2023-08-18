import logging
from database import Database


logger = logging.getLogger(__name__)


class TableHandler:

    def __init__(
            self,
            db: Database,
            name: str,
            keys: "tuple[str]",
            description: str,
            ) -> None:
        # Members
        self._db = db
        self._name = name
        self._keys = keys
        self._description = description
        #

        # If table does not exist, create one
        if not self.is_table():
            self.create_table()

        #
        logger.info(f'{self.__class__.__name__} for {name} initialized correctly')
        pass

    def is_table(self) -> bool:
        """Checks if table exists

        Returns:
            bool: True if exists
        """
        return self._db.is_table(
            name=self._name
        )

    def check_table_format(self) -> bool:
        # is it in correct format
        # TODO: implement me
        raise NotImplementedError()

    def create_table(self):
        """Create table according to description
        """
        return self._db.create_table(
            name=self._name,
            description=self._description
        )

    pass
