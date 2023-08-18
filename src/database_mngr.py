import pymysql
import logging


logger = logging.getLogger(__name__)


class DatabaseMngr:

    def __init__(
            self,
            host: str,
            port: int,
            user: str,
            password: str,
            name: str,
            ) -> None:
        # Members
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._name = name
        #
        self._connection = None
        #
        self.connect()
        pass

    def connect(self) -> None:
        """Connet mysql object
        """
        if not self._connection:
            self._connection = pymysql.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                port=self._port,
                database=self._name
            )
            logger.debug(f'DatabaseMngr {self._name} connected')

    def disconnect(self) -> None:
        """Disconnet mysql object
        """
        if self._connection:
            self._connection.close()
            logger.debug(f'DatabaseMngr {self._name} disconnected')

    def is_table(self, name: str) -> bool:
        """Checks if table {name} exists
        """
        return name in self.get_table_names()

    def create_table(self, name: str, description: str, options: str = None):
        """Create mySQL table

        Args:
            name (str): Name of the table
            description (str): Description of table - content od parentheses
            options (str): Additional options to table. Defaults to None (empty string)
        """
        options = options if options else ''
        query = f"CREATE TABLE {name} ({description}) {options};"
        with self._connection.cursor() as cursor:
            cursor.execute(query)
        logger.debug(f'Created new table "{name}" in database {self._name}')

    def get_data(self, name: str) -> "tuple[tuple, tuple]":
        """Get all rows from table

        Args:
            name (str): Name of the table read from

        Returns:
            tuple[tuple, tuple]: column_names, rows
        """
        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = f"SELECT * FROM {name}"
            cursor.execute(query)
            columns = cursor.description
            column_names = [elem[0] for elem in columns]
            table = cursor.fetchall()
            return column_names, table

    def get_data_with_condition(self, name: str, condition: str) -> "tuple[tuple, tuple]":
        """Get all rows from table that satisfy condition

        Args:
            name (str): Name of the table read from
            condition (str): Condition to satisfy

        Returns:
            tuple[tuple, tuple]: column_names, rows
        """
        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = f"SELECT * FROM {name} WHERE {condition};"
            cursor.execute(query)
            columns = cursor.description
            column_names = [elem[0] for elem in columns]
            table = cursor.fetchall()
            return column_names, table

    def get_table_names(self):
        """Get all table names from database
        """
        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = "SHOW TABLES"
            cursor.execute(query)
            # Fetch all the table names
            tables = cursor.fetchall()
            ret = [t[0] for t in tables]
            return ret

    def insert_entry(self, name: str, keys: "tuple[str]", data: tuple):
        # TODO: Maybe dict should represent data?

        # Create strings from tuple
        keys = ', '.join(keys)  # 'name, surname, age'
        values = ', '.join(['%s'] * len(keys))  # '%s, %s, %s'
        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = f"INSERT INTO {name} ({keys}) VALUES ({values})"
            cursor.execute(query, data)
            self._connection.commit()
            # id of last added entry
            return cursor.lastrowid

    def insert_entries(self, name: str, keys: "tuple[str]", data: "tuple[tuple]"):
        # TODO: Maybe dict should represent data?

        # Create strings from tuple
        keys = ', '.join(keys)  # 'name, surname, age'
        values = ', '.join(['%s'] * len(keys))  # '%s, %s, %s'

        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = f"INSERT INTO {name} ({keys}) VALUES ({values})"
            cursor.executemany(query, data)
            self._connection.commit()
            # id of last added entry
            return cursor.lastrowid

    pass


if __name__ == '__main__':
    #
    db = DatabaseMngr(
        host='192.168.100.196',
        port=3307,
        user='organizer',
        password='UhU*K89AOWx#X41d',
        name='organizer_db',
    )
    # Show existing tables
    print('Existing tables:', db.get_table_names())
    # Check if table exists
    for name in ['containers', 'elements']:
        exists = db.is_table(name)
        print(f'Table {name} exists: {exists}')
        # Create table
        if not exists:
            description = "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT"
            db.create_table(name, description)
        # Print table
        if exists:
            column_names, table = db.get_data(name)
            print(column_names)
            for row in table:
                print(row)
            print()

            # # Insert single data
            # keys = ('name', 'age')
            # data = ('Tomek', 24)
            # db.insert_entry(name, keys, data)

            # # Insert data
            # keys = ('name', 'age')
            # data = (
            #     ('Tomek', 21),
            #     ('Alfons', 22),
            #     ('Fredek', 23),
            #     ('Zgredek', 24),
            #     ('Runcajs', 25),
            # )
            # db.insert_entries(name, keys, data)

    # Disconect from db
    db.disconnect()
    pass
