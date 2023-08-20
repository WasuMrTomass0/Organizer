import sqlalchemy as sql
from sqlalchemy.orm import declarative_base


# ORM base class
Base = declarative_base()


class Container(Base):
    __tablename__ = 'containers'
    __table_args__ = {'extend_existing': True}

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    location = sql.Column(sql.String)
    description = sql.Column(sql.Text)

    def __str__(self) -> str:
        return f'Container: id({self.id}), location({self.location}), description({self.description})'
