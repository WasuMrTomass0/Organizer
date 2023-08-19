"""
Test/Sandbox file used for manual testing
"""
import logging.config
logging.config.fileConfig('logging.conf')

from database.database_mngr import DatabaseMngr
from database.table_mngr import TableMngr


# Containers table
T_CONT_NAME = 'containers'
T_CONT_KEYS = ('id', 'location', 'description')
T_CONT_DESC = """
id INT AUTO_INCREMENT NOT NULL,
location VARCHAR(255),
description TEXT,

PRIMARY KEY (id)
"""


# Create database handler
db = DatabaseMngr(
    host='localhost',
    port=3306,
    user='root',
    password='',
    name='organizer_db',
)
# db = DatabaseMngr(
#     host='192.168.100.196',
#     port=3307,
#     user='organizer',
#     password='UhU*K89AOWx#X41d',
#     name='organizer_db',
# )

def main():
    
    with db:
        if not db.is_table(name=T_CONT_NAME):
            db.create_table(name=T_CONT_NAME, description=T_CONT_DESC)

        db.insert_entry(
            name=T_CONT_NAME,
            keys=['location', 'description'],
            data=['Attic', 'Some information here']
        )
        pass

    pass


if __name__ == '__main__':
    main()
