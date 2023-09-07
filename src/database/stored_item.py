import sqlalchemy as sql
from sqlalchemy.sql import func

from database.base import Base
from database.container import Container


class StoredItem(Base):
    __tablename__ = 'stored_items'
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

    __tableformula__ = '' \
        'CREATE TABLE stored_items (' \
        '   id INT AUTO_INCREMENT NOT NULL,' \
        '   containerid INT NOT NULL,' \
        '   name VARCHAR(255) NOT NULL,' \
        '   description TEXT,' \
        '   quantity INT NOT NULL,' \
        '   image MEDIUMBLOB,' \
        '   created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,' \
        '   edited TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,' \
        '   PRIMARY KEY (id),' \
        '   KEY (containerid),' \
        '   FOREIGN KEY (containerid) REFERENCES containers(id)' \
        ') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'
