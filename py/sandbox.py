"""
Test/Sandbox file used for manual testing
"""
import logging.config
logging.config.fileConfig('logging.conf')

from database import Database
from table_handler import TableHandler


# Containers table
T_CONT_NAME = 'containers'
T_CONT_KEYS = ('id', 'name', 'location', 'description')
T_CONT_DESC = """
id INT AUTO_INCREMENT NOT NULL,
name VARCHAR(255) NOT NULL,
location VARCHAR(255),
description TEXT,

PRIMARY KEY (id)
"""
# Elements table
T_ELEM_NAME = 'elements'
T_ELEM_KEYS = ('id', 'containerid', 'name', 'description', 'image', 'created', 'edited')
T_ELEM_DESC = """
id INT AUTO_INCREMENT NOT NULL,
containerid INT,
name VARCHAR(255) NOT NULL,
description TEXT,
image MEDIUMBLOB,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
edited TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

PRIMARY KEY (id),
CONSTRAINT FK_containerid FOREIGN KEY (containerid) REFERENCES containers(id)
"""


def main():
    # Initialize logger
    import logging
    logger = logging.getLogger(__name__)

    logger.debug(f'Test message')
    logger.info(f'Test message')
    logger.warning(f'Test message')
    logger.error(f'Test message')

    # Create database handler
    db = Database(
        host='192.168.100.196',
        port=3307,
        user='organizer',
        password='UhU*K89AOWx#X41d',
        name='organizer_db',
    )

    # Create table handler - containers
    tb_containers = TableHandler(
        db=db,
        name=T_CONT_NAME,
        keys=T_CONT_KEYS,
        description=T_CONT_DESC
    )
    # Create table handler - elements
    tb_elements = TableHandler(
        db=db,
        name=T_ELEM_NAME,
        keys=T_ELEM_KEYS,
        description=T_ELEM_DESC
    )

    pass


if __name__ == '__main__':
    main()
