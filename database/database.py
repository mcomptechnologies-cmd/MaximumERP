import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("maximumerp.db")
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            barcode TEXT UNIQUE,

            item_name TEXT,

            category TEXT,

            quantity INTEGER,

            buying_price REAL,

            selling_price REAL

        )
        """)

        self.conn.commit()


db = Database()