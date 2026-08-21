from PyQt6.QtSql import QSqlDatabase,QSqlQuery
from custom_exceptions.database_exception import DatabaseException


class DatabaseService():
    """
        Constructor that initialize the DatabaseService instances
        which uses SQlite  by default.
    """
    def __init__(self, db_type="QSQLITE") -> None:
        self.database_name = "cua.sqlite"
        self.conn = QSqlDatabase.addDatabase(db_type)
        self.conn.setDatabaseName(self.database_name)

    def connect(self) -> None:
        """
            Open the database and establish connection for further queries
        """
        if not self.conn.isOpen():
            self.conn.open()

    def disconnect(self) -> None:
        """
            Checks if the database open then if it is, it will disconnect and don nothing otherwise
        """
        if self.conn.isOpen():
            self.conn.close()

    def add_table(self, table_names: list):
        """
            Add new tables with the table_name
        """
        if len(table_names) == 2:
            try:
                if not self.conn.isOpen():
                    self.connect()
                if table_names[0] not in self.conn.tables() and table_names[1] not in self.conn.tables():
                    query_1 = QSqlQuery(
                        f"CREATE TABLE {table_names[0]} (user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name VARCHAR(50) NOT NULL, created_at DATE);" 
                        ,db=self.conn)
                    query_2 = QSqlQuery(
                        f"""CREATE TABLE {table_names[1]} (
                            history_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            user_id INTEGER NOT NULL,
                            history_name VARCHAR(50) NOT NULL, 
                            history_value INTEGER NOT NULL,
                            updated_at DATE NOT NULL,
                            history_deleted BOOLEAN DEFAULT FALSE,
                            FOREIGN KEY(user_id) REFERENCES users(user_id)
                            )
                        """,
                        db=self.conn)

                    db_response_2 = query_2.exec()
                    db_response_1 = query_1.exec()
                   

                    if db_response_1 and db_response_2:
                        print(f"{table_names[0]} and {table_names[1]} tables are created")
                    else:
                        print(f"Unable to create tables {table_names[0]} and {table_names[1]}")
                else:
                    print(f"The {table_names[0] and table_names[1]} are table already exist")
                self.disconnect()
            except Exception as e:
                raise DatabaseException(f"Error occured while creating a table.\nError: {e}")
        else:
            raise DatabaseException("Missing table name")

    def create_user(self, username: str, created_at: str) -> bool:
        """
            Creates a new user with the given username. It also keep the timestamp
            for the new created user.

            username: a string value which represents the user username
            created_at: a string representation of a Python date(YYYY,MM,DD)
        """
        if not username and not created_at:
            raise DatabaseException("Username and created date is missing.")
        else:
            try:
                if not self.conn.isOpen():
                    self.connect()

                query = QSqlQuery(db=self.conn)
                query.prepare("INSERT INTO users (user_name, created_at) VALUES (?,?);")
                query.bindValue(0, username)
                query.bindValue(1, str(created_at))

                db_response = query.exec()

                if db_response:
                    print("User data created.")
                    self.disconnect()
                    return True
                
                self.disconnect()
                
            except Exception as e:
                self.disconnect()
                raise DatabaseException(f"Unbale to save user informations.\nError: {e}")
            return False
            
    def read_a_user(self, username: str) -> tuple|None:
        """
            Retrieve a single user with the given username if exists. If a user found 
            the user information is returned as tuple. Otherwise None is returned.

            username: a string value which is being searched for in the user database
        """
        if username:
            try:
                if not self.conn.isOpen():
                    self.connect()

                query = QSqlQuery(db=self.conn)
                query.prepare(f"SELECT * FROM users WHERE user_name=?")
                query.addBindValue(username)
                db_response = query.exec()

                if db_response:
                    user_data = None
                    while query.next():
                        user_data = query.value(0), query.value(1), query.value(2), query.value(3)
                    self.disconnect()
                    return user_data
                self.disconnect()
            except Exception as e:
                raise DatabaseException(f"Unable to read user information.\nError: {e}")
        else:
            raise DatabaseException("Missing table name or username information while reading user data")
        return None
    
    def read_all_users(self) -> list:
        """
            Retrives all the user data from the database and return them as a list
        """
        user_data = []
        try:
            if not self.conn.isOpen():
                self.connect()
            query = QSqlQuery(f"SELECT * FROM users", db=self.conn)
            db_response = query.exec()

            if db_response:
                while query.next():
                    user_data.append((query.value(0), query.value(1), query.value(2)))
                self.disconnect()
            else:
                self.disconnect()
                raise DatabaseException(f"Unable to read all data from table users")
        except Exception as e:
            self.disconnect()
            raise DatabaseException(f"Error occurred while retrieving all data.\nError {e}")
        return user_data

    def create_history(self, username: str, history_name: str, history_value: float, updated_at: str) -> bool:
        """
            Creates a new history in the database and returns a boolean value to show the success and failure of database operation.
            username: a string value which represent the user username the history stored for
            history_name: a string value which represent what type of history it is. For instance counter value, calculations, etc ...
            history_value: a numerical value represent the value of the history to be saved
            updated_at: a string representation of Python date(YYYY,MM,DD) which represent when the history is created
        """
        db_response = False

        if not history_name and not history_value:
            raise DatabaseException("History name or history value is missing while creating history")
        else:
            try:
                user = self.read_a_user(username)
                if user:
                    if not self.conn.isOpen():
                        self.connect()

                    query = QSqlQuery(db=self.conn)
                    query.prepare(
                        """
                            INSERT INTO history(user_id, history_name, history_value, updated_at) VALUES(?,?,?,?)
                        """
                    )
                    query.bindValue(0, user[0])
                    query.bindValue(1, history_name)
                    query.bindValue(2, history_value)
                    query.bindValue(3, str(updated_at))

                    db_response = query.exec()
                    if db_response:
                        self.disconnect()
                        print("User history created")
                self.disconnect()
            except Exception as e:
                raise DatabaseException(f"Error occured while saving user history.\nError: {e}")
            return db_response

    def read_all_history(self, username: str) -> list:
        """
            Retrieves the history name, history value and updated date as a list if it exists
            for a given username
        """
        user_history = []
        user = self.read_a_user(username)
        if user:
            try:
                if not self.conn.isOpen():
                    self.conn.open()
                query = QSqlQuery(db=self.conn)
                query.prepare(
                    f"""
                        SELECT * FROM history WHERE user_id={user[0]}
                    """
                )
                db_response = query.exec()
                if db_response:
                    while query.next():
                        if query.value(5) == 0:
                            user_history.append((query.value(2), query.value(3), query.value(4)))
                self.disconnect()

            except Exception as e:
                raise DatabaseException(f"Error: {e}")
        return user_history
        
    def update_user(self):
        ...
    def update_history(self):
        ...
    def delete_a_user(self):
        ...
    def delete_history(self):
        ...