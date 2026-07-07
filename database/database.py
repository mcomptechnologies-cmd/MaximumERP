import mysql.connector


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin123",
            database="maximum_erp"
        )

        self.cursor = self.conn.cursor(dictionary=True)

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory(
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(200),
            category VARCHAR(100),
            quantity INT,
            buying_price DECIMAL(10,2),
            selling_price DECIMAL(10,2)
        )
        """)

        self.conn.commit()

    # ==========================
    # Inventory Functions
    # ==========================

    def add_product(self, product, category, quantity, buying, selling):
        sql = """
        INSERT INTO inventory
        (product_name, category, quantity, buying_price, selling_price)
        VALUES (%s,%s,%s,%s,%s)
        """

        values = (
            product,
            category,
            quantity,
            buying,
            selling
        )

        self.cursor.execute(sql, values)
        self.conn.commit()

    def get_products(self):
        self.cursor.execute("SELECT * FROM inventory ORDER BY id DESC")
        return self.cursor.fetchall()

    def delete_product(self, product_id):
        self.cursor.execute(
            "DELETE FROM inventory WHERE id=%s",
            (product_id,)
        )
        self.conn.commit()

    def update_product(self, product_id, product, category,
                       quantity, buying, selling):

        sql = """
        UPDATE inventory
        SET
        product_name=%s,
        category=%s,
        quantity=%s,
        buying_price=%s,
        selling_price=%s
        WHERE id=%s
        """

        self.cursor.execute(sql, (
            product,
            category,
            quantity,
            buying,
            selling,
            product_id
        ))

        self.conn.commit()


db = Database()
db.create_tables()
def search_products(self, keyword):

    sql = """
    SELECT *
    FROM inventory
    WHERE product_name LIKE %s
    OR category LIKE %s
    ORDER BY id DESC
    """

    value = "%" + keyword + "%"

    self.cursor.execute(sql, (value, value))

    return self.cursor.fetchall()