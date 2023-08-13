from database import Database


class TableHandler:

    def __init__(
            self,
            db: Database,
            name: str,
            keys: str,
            description: str,
            ) -> None:
        # Members
        self._db = db
        self._name = name
        self._keys = keys
        self._description = description
        # 
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
        """Create table accoring to description
        """
        return self._db.create_table(
            name=self._name,
            description=self._description
        )

    pass
