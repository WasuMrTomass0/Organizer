import sqlalchemy as sql
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from database.container import Container

# ORM base class
Base = declarative_base()


class StoredItem(Base):
    __tablename__ = 'stored_items'
    __table_args__ = {'extend_existing': True}

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    containerid = sql.Column(sql.Integer, sql.ForeignKey(Container.id))
    name = sql.Column(sql.String)
    description = sql.Column(sql.Text)
    image = sql.Column(sql.BLOB)
    created = sql.Column(sql.TIMESTAMP, server_default=func.now())
    edited = sql.Column(sql.TIMESTAMP, onupdate=func.now())
    
    def __str__(self) -> str:
        return f'StoredItem: ' \
            f'id({self.id}), containerid({self.containerid}), ' \
            f'name({self.name}), description({self.description}), ' \
            f'image({(len(self.image) if self.image else self.image)}), ' \
            f'created({self.created}), edited({self.edited})'
