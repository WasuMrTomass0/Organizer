import sqlalchemy as sql
from sqlalchemy.sql import func

from database.base import Base
from database.container import Container
from database.stored_item import StoredItem


class ItemInUse(Base):
    __tablename__ = 'items_in_use'
    __table_args__ = {'extend_existing': True}

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    containerid = sql.Column(sql.Integer, sql.ForeignKey(Container.id))
    name = sql.Column(sql.String)
    description = sql.Column(sql.Text)
    quantity = sql.Column(sql.Integer)
    image = sql.Column(sql.BLOB)
    created = sql.Column(sql.TIMESTAMP, server_default=func.now())
    edited = sql.Column(sql.TIMESTAMP, onupdate=func.now())

    def __str__(self) -> str:
        return f'StoredItem: ' \
            f'id({self.id}), containerid({self.containerid}), ' \
            f'name({self.name}), description({self.description}), ' \
            f'quantity({self.quantity}), ' \
            f'image({(len(self.image) if self.image else self.image)}), ' \
            f'created({self.created}), edited({self.edited})'

    @staticmethod
    def from_stored_item(si: StoredItem) -> "ItemInUse":
        return ItemInUse(
            id=si.id,
            containerid=si.containerid,
            name=si.name,
            description=si.description,
            quantity=si.quantity,
            image=si.image,
            created=si.created,
            edited=si.edited,
        )
