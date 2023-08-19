import mysql.connector
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
        self._connection = None  # type: mysql.connector.MySQLConnection
        pass

    def __enter__(self):
        """Connect to database. Return self
        """
        self._connect()
        return self

    def __exit__(self, *args):
        """Disconnect from database
        """
        self._disconnect()

    def __bool__(self) -> bool:
        """Is connection to database active
        """
        return self.is_connected()

    def _connect(self) -> None:
        """Connet mysql object
        """
        # If not already connected
        if not self.is_connected():
            try:
                # Connect to existing database
                self._connection = mysql.connector.connect(
                    host=self._host,
                    user=self._user,
                    password=self._password,
                    port=self._port,
                    database=self._name
                )
            except mysql.connector.errors.ProgrammingError or mysql.connector.errors.MySQLInterfaceError:
                logger.info(f'Database "{self._name}" does not exist')
                self._create_database()
                # Rerun this method
                return self._connect()
            except mysql.connector.errors.DatabaseError as err:
                logger.fatal(f'Database "{self._name}" - could not connect')
                raise err

            logger.info(f'Database "{self._name}" connected')

    def _disconnect(self) -> None:
        """Disconnet mysql object
        """
        if self._connection:
            self._connection.close()
            logger.info(f'Database "{self._name}" disconnected')

    def _create_database(self) -> None:
        """Create database
        """
        try:
            # Create connection to database
            self._connection = mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                port=self._port
            )
        except mysql.connector.errors.DatabaseError as err:
            logger.fatal(f'Database "{self._name}" - could not connect')
            raise err
        # Create database
        query = f'CREATE DATABASE {self._name}'
        logger.debug(f'Database "{self._name}" - querry: {query}')
        with self._connection.cursor() as cursor:
            cursor.execute(query)
        logger.info(f'Database "{self._name}" created')

    def is_connected(self) -> bool:
        return self._connection is not None and self._connection.is_connected()

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
        logger.debug(f'Database "{self._name}" - querry: {query}')
        with self._connection.cursor() as cursor:
            cursor.execute(query)
        logger.info(f'Database "{self._name}" - created new table "{name}"')

    def get_data(self, name: str, limit: int = None, condition: str = None) -> "tuple[tuple, tuple]":
        """Get all rows from table

        Args:
            name (str): Name of the table read from
            limit (int): Limit of returned entries
            condition (str): Condition string

        Returns:
            tuple[tuple, tuple]: column_names, rows
        """
        # Check inputs
        limit = 0 if limit is None else limit
        if limit < 0:
            logger.error(f'Database "{self._name}" - received invalid limit value ({limit})')
            limit = 0
        # Create query
        limit_q = f'LIMIT {limit}' if limit else ''
        condition_q = f'WHERE {condition}' if condition else ''
        query = f"SELECT * FROM {name} {limit_q} {condition_q}"
        logger.debug(f'Database "{self._name}" - querry: {query}')
        # Execute
        with self._connection.cursor() as cursor:
            cursor.execute(query)
            table = cursor.fetchall()
            columns = cursor.description
        column_names = [elem[0] for elem in columns]
        return column_names, table

    def get_table_names(self):
        """Get all table names from database
        """
        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = "SHOW TABLES"
            logger.debug(f'Database "{self._name}" - querry: {query}')
            cursor.execute(query)
            # Fetch all the table names
            tables = cursor.fetchall()
            ret = [t[0] for t in tables]
            return ret

    def insert_entry(self, name: str, keys: "tuple[str]", data: tuple):
        # TODO: Maybe dict should represent data?

        # Create strings from tuple
        values = ', '.join(['%s'] * len(keys))  # '%s, %d, %s'
        keys = ', '.join(keys)  # 'name, surname, age'
        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = f"INSERT INTO {name} ({keys}) VALUES ({values})"
            logger.debug(f'Database "{self._name}" - querry: {query}')
            cursor.execute(query, data)
            self._connection.commit()
            # id of last added entry
            return cursor.lastrowid

    def insert_entries(self, name: str, keys: "tuple[str]", data: "tuple[tuple]"):
        # TODO: Maybe dict should represent data?

        # Create strings from tuple
        values = ', '.join(['%s'] * len(keys))  # '%s, %s, %s'
        keys = ', '.join(keys)  # 'name, surname, age'

        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = f"INSERT INTO {name} ({keys}) VALUES ({values})"
            logger.debug(f'Database "{self._name}" - querry: {query}')
            cursor.executemany(query, data)
            self._connection.commit()
            # id of last added entry
            return cursor.lastrowid

    pass
