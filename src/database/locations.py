import sqlalchemy as sql

from database.base import Base


class Location(Base):
    __tablename__ = 'locations'
    __table_args__ = {'extend_existing': True}

    name = sql.Column(sql.String, primary_key=True)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f'Location: name({self.name})'
