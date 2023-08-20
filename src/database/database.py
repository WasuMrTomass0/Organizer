from typing import Any, Iterable

import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func

from database.container import Container
from database.stored_item import StoredItem


class Database:

    def __init__(self) -> None:
        # scheme://username:password@host/database?params
        self._engine = sql.create_engine('mysql+pymysql://root:@localhost:3306/organizer_db')
        self._connector = self._engine.connect()
        self._SessionClass = sessionmaker(bind=self._engine)
        self._open_session()

    def _open_session(self) -> None:
        self._session = self._SessionClass()

    def _close_session(self) -> None:
        self._session.close()

    def _insert_single(self, obj) -> None:
        query = self._session.query(obj.__class__)
        self._session.add(obj)
        self._session.commit()

    def _insert_many(self, objs) -> None:
        obj = objs[0]
        query = self._session.query(obj.__class__)
        for obj in objs:
            self._session.add(obj)
        self._session.commit()

    def is_table(self, cls: str) -> bool:
        """Check if table exists

        Args:
            cls (str): Class type corelated with table - must containt __tablename__
        """
        return sql.inspect(self._engine).has_table(cls.__tablename__)

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

    def get(self, cls, limit: int = None, condition = None):
        """Get entry rows from

        Args:
            cls (Class): Class type corelated with table

        Returns:
            List: Entries
        """
        query = self._session.query(cls)
        if limit:
            query = query.limit(limit)
        if condition is not None:
            query = query.where(condition)
        return query.all()

    def update(self, obj) -> None:
        """Update object in database. Method uses object's id to match updated entry

        Args:
            obj (_type_): _description_
        """
        condition = obj.__class__ == obj.id
        data = self.get(obj.__class__, condition)
        data[0] = obj
        self._session.commit()


# db = Database()

# print(db.is_table(Container))
# print(db.is_table(StoredItem))

# for e in db.get(Container, condition=Container.id < 5):
#     print(str(e))


# for e in db.get(StoredItem):
#     print(str(e))

# s = StoredItem()
# s.containerid = 1
# s.name = 'Some trousers'
# s.description = 'Some info here'
# db.insert(s)

# import time
# time.sleep(4)

# s.name = 'Some blue trousers'
# db.update(s)

# query = ses.query(StoredItem).limit(5)
# query
# print(f'{query = }')
# for q in query.all():
#     print(q.id, q.location, q.description)


# New element
# c = Container()
# c.location = 'Garage'
# c.description = 'Some description here'
# ses.add(c)
# ses.commit()

# # New element
# query = ses.query(StoredItem)
# s = StoredItem()
# s.containerid = 1
# s.name = 'Jacket'
# s.description = 'Winter Jacket'

# ses.add(s)
# ses.commit()

# # Edit element
# query = ses.query(Container).limit(5)
# q = query.all()[0]
# q.location = 'Main room'
# ses.commit()

# query = ses.query(Container).limit(5)
# print(f'{query = }')
# for q in query.all():
#     print(q.id, q.location, q.description)
