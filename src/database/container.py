import sqlalchemy as sql

from database.base import Base
from database.locations import Location


class Container(Base):
    __tablename__ = 'containers'
    __table_args__ = {'extend_existing': True}

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    location = sql.Column(sql.String, sql.ForeignKey(Location.name))
    description = sql.Column(sql.Text)

    def __str__(self) -> str:
        return f'Container_{self.id}'

    def __repr__(self) -> str:
        return f'Container: id({self.id}), location({self.location}), description({self.description})'
