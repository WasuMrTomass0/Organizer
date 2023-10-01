from typing import Any, Iterable

import sqlalchemy as sql
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists


class Database:

    def __init__(
            self,
            username: str = None,
            password: str = None,
            host: str = None,
            port: int = None,
            database: str = None,
            # params: dict = None,
        ) -> None:
        # Read data
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.url = self._create_engine_url()
        # self.params = params

        # Initialize database
        if not self._is_database():
            self._create_database()
        self._connect_to_database()
        self._open_session()

    def _create_engine_url(self) -> str:
        # scheme://username:password@host/database?params
        scheme = 'mysql+pymysql'
        return f'{scheme}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'

    def _is_database(self) -> bool:
        return database_exists(url=self.url)

    def _create_database(self) -> None:
        create_database(url=self.url, encoding='utf8mb4')

    def _connect_to_database(self) -> None:
        self._engine = sql.create_engine(url=self.url)
        self._connector = self._engine.connect()
        self._SessionClass = sessionmaker(bind=self._engine)
        self._session = None

    def __enter__(self):
        self._open_session()

    def __exit__(self, *args):
        self._close_session()

    def _commit(self) -> None:
        self._session.commit()

    def _open_session(self) -> None:
        if self._session:
            self._session.rollback()
        self._session = self._SessionClass()

    def _close_session(self) -> None:
        self._session.close()

    def _insert_single(self, obj) -> None:
        query = self._session.query(obj.__class__)
        self._session.add(obj)
        self._commit()

    def _insert_many(self, objs) -> None:
        obj = objs[0]
        query = self._session.query(obj.__class__)
        for obj in objs:
            self._session.add(obj)
        self._commit()

    def _remove_single(self, cls, condition) -> None:
        self._session.query(cls).filter(condition).delete()
        self._commit()

    def _insert_many(self, objs) -> None:
        raise NotImplementedError()

    def is_table(self, cls: str) -> bool:
        """Check if table exists

        Args:
            cls (str): Class type corelated with table - must containt __tablename__
        """
        return sql.inspect(self._engine).has_table(cls.__tablename__)

    def create_table(self, cls: str) -> None:
        """Create table for ORM class

        Args:
            cls (str): Class type corelated with table - must containt __tableformula__
        """
        self.execute(query=text(cls.__tableformula__))

    def execute(self, query: str):
        """Execute sql query and return result
        """
        return self._session.execute(query)

    def insert(self, obj: "Any | Iterable[Any]") -> None:
        """Insert entry data to table

        Args:
            obj (EntryDataType | Iterable[EntryDataType]): Entry data type corelated with table.
        """
        if isinstance(obj, tuple) or isinstance(obj, list):
            return self._insert_many(objs=obj)
        else:
            return self._insert_single(obj=obj)

    def remove(self, cls, conditions: list) -> None:
        """Remove entries from table

        Args:
            cls (class): Entry data type
            conditions (list): Conditions used to match entries
        """
        for con in conditions:
            return self._remove_single(cls=cls, condition=con)

    def get(self, cls, limit: int = None, conditions: list = None) -> list:
        """
        Get entry rows from

        Args:
            cls (Class): Class type corelated with table
            limit (int, optional): _description_. Defaults to None.
            conditions (list, optional): _description_. Defaults to None.

        Returns:
            List: Entries
        """
        query = self._session.query(cls)
        if limit:
            query = query.limit(limit)
        if conditions:
            query = query.where(*conditions)
        return query.all()

    def update(self, obj) -> None:
        """Update object in database. Method uses object's id to match updated entry

        Args:
            obj (_type_): _description_
        """
        condition = obj.__class__ == obj.id
        data = self.get(obj.__class__, condition)
        data[0] = obj
        self._commit()

    def count(self, cls) -> int:
        """Count elements in table

        Args:
            cls (Class): Class type corelated with table

        Returns:
            int: Quantity
        """
        return self._session.query(cls).count()
