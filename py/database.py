import pymysql


class Database:

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
        if not self._connection:
            self._connection = pymysql.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                port=self._port,
                database=self._name
            )

    def disconnect(self) -> None:
        if self._connection:
            self._connection.close()

    def is_table(self, name: str):
        return name in self.get_tables()

    def create_table(self, name: str, description: str):
        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = f"CREATE TABLE {name} ({description})"
            cursor.execute(query)

    def get_table(self, name: str):
        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = f"SELECT * FROM {name}"
            cursor.execute(query)
            columns = cursor.description
            column_names = [elem[0] for elem in columns]
            table = cursor.fetchall()
            return column_names, table

    def get_table_names(self):
        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = "SHOW TABLES"
            cursor.execute(query)
            # Fetch all the table names
            tables = cursor.fetchall()
            ret = [t[0] for t in tables]
            return ret

    def insert_single_data(self, name: str, keys: str, data: tuple):
        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = f"INSERT INTO {name} ({keys}) VALUES (%s, %s)"
            cursor.execute(query, data)
            self._connection.commit()
            # id of last added entry
            return cursor.lastrowid

    def insert_data(self, name: str, keys: str, data: tuple[tuple]):
        # Create a cursor object to interact with the database
        with self._connection.cursor() as cursor:
            # SQL query to show all tables in the specified database
            query = f"INSERT INTO {name} ({keys}) VALUES (%s, %s)"
            cursor.executemany(query, data)
            self._connection.commit()
            # id of last added entry
            return cursor.lastrowid

    pass


if __name__ == '__main__':
    # 
    db = Database(
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
            column_names, table = db.get_table(name)
            print(column_names)
            for row in table:
                print(row)
            print()

            # # Insert single data
            # keys = "name, age"
            # data = ('Tomek', 24)
            # db.insert_single_data(name, keys, data)

            # # Insert data
            # keys = "name, age"
            # data = (
            #     ('Tomek', 21),
            #     ('Alfons', 22),
            #     ('Fredek', 23),
            #     ('Zgredek', 24),
            #     ('Runcajs', 25),
            # )
            # db.insert_data(name, keys, data)

    # Disconect from db
    db.disconnect()
    pass
