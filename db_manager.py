import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self):
        self.conn = None

    def connect(self):
        """Establish a database connection."""
        if self.conn is None:
            try:
                self.conn = mysql.connector.connect(
                    host="",
                    user="",
                    passwd="",
                    database="",
                    port=0000
                )
            except Error as e:
                print(f"Error connecting to the database: {e}")


    def disconnect(self):
        """Close the database connection."""
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()
            self.conn = None

    def execute_query(self, query, params=None):
        """Execute a query."""
        self.connect()
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query, params)
                self.conn.commit()
                return cursor.lastrowid
            except Error as e:
                print(f"Error executing query: {e}")

    def fetch_query(self, query, params=None):
        """Fetch a single record from the database."""
        self.connect()
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()  # Fetch the first row