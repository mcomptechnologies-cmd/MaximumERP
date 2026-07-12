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

    # ==========================================
    # CREATE TABLES
    # ==========================================

    def create_tables(self):

        # Inventory Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory(
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(200),
            category VARCHAR(100),
            serial_number VARCHAR(100),
            quantity INT,
            buying_price DECIMAL(10,2),
            selling_price DECIMAL(10,2)
        )
        """)
        # Customers Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(200),
            phone VARCHAR(50),
            email VARCHAR(100),
            address TEXT
        )
        """)
        # Sales Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales(
            id INT AUTO_INCREMENT PRIMARY KEY,
            invoice_no VARCHAR(30),
            customer VARCHAR(200),
            sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            total DECIMAL(10,2)
        )
        """)
        # Serial Numbers Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS serial_numbers(
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT,
            serial_number VARCHAR(150) UNIQUE,
            status VARCHAR(30) DEFAULT 'In Stock'
        )
        """)
        # Repairs Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS repairs(
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer VARCHAR(200),
            device VARCHAR(200),
            problem TEXT,
            status VARCHAR(50)
        )
        """)
        # Sale Items Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale_items(
            id INT AUTO_INCREMENT PRIMARY KEY,
            sale_id INT,
            product_id INT,
            product_name VARCHAR(200),
            quantity INT,
            price DECIMAL(10,2),
            total DECIMAL(10,2)
        )
        """)

        self.conn.commit()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(200),
            phone VARCHAR(50),
            email VARCHAR(100),
            address TEXT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS repairs(
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer VARCHAR(200),
            device VARCHAR(200),
            problem TEXT,
            status VARCHAR(50)
        )
        """)
    # ==========================================
    # INVENTORY METHODS
    # ==========================================

    def add_product(self, product, category, quantity, buying, selling):

        sql = """
        INSERT INTO inventory
        (product_name, category, quantity, buying_price, selling_price)
        VALUES (%s, %s, %s, %s, %s)
        """

        self.cursor.execute(sql, (
            product,
            category,
            quantity,
            buying,
            selling
        ))

        self.conn.commit()

    def get_products(self):

        self.cursor.execute(
            "SELECT * FROM inventory ORDER BY id DESC"
        )

        return self.cursor.fetchall()

    def update_product(
        self,
        product_id,
        product,
        category,
        quantity,
        buying,
        selling
    ):

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

    def delete_product(self, product_id):

        self.cursor.execute(
            "DELETE FROM inventory WHERE id=%s",
            (product_id,)
        )

        self.conn.commit()

    def search_products(self, keyword):

        sql = """
        SELECT *
        FROM inventory
        WHERE product_name LIKE %s
           OR category LIKE %s
        ORDER BY id DESC
        """

        value = f"%{keyword}%"

        self.cursor.execute(sql, (value, value))

        return self.cursor.fetchall()
    # ==========================================
    # DASHBOARD METHODS
    # ==========================================

    def inventory_count(self):
        self.cursor.execute("SELECT COUNT(*) AS total FROM inventory")
        return self.cursor.fetchone()["total"]

    def customers_count(self):
        self.cursor.execute("SELECT COUNT(*) AS total FROM customers")
        result = self.cursor.fetchone()
        return result["total"] if result else 0

    def total_sales(self):
        self.cursor.execute("SELECT IFNULL(SUM(total),0) AS total FROM sales")
        result = self.cursor.fetchone()
        return result["total"] if result else 0

    def repairs_count(self):
        self.cursor.execute("SELECT COUNT(*) AS total FROM repairs")
        result = self.cursor.fetchone()
        return result["total"] if result else 0
    def inventory_count(self):

        self.cursor.execute(
            "SELECT COUNT(*) AS total FROM inventory"
        )

        result = self.cursor.fetchone()

        return result["total"] if result else 0
    # ==========================================
    # SALES METHODS
    # ==========================================

    def save_sale(self, invoice_no, customer, total):

        sql = """
        INSERT INTO sales
        (invoice_no, customer, total)
        VALUES (%s, %s, %s)
        """

        self.cursor.execute(sql, (
            invoice_no,
            customer,
            total
        ))

        self.conn.commit()

        return self.cursor.lastrowid

    def save_sale_item(
        self,
        sale_id,
        product_id,
        product_name,
        quantity,
        price,
        total
    ):

        sql = """
        INSERT INTO sale_items
        (
            sale_id,
            product_id,
            product_name,
            quantity,
            price,
            total
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        self.cursor.execute(sql, (
            sale_id,
            product_id,
            product_name,
            quantity,
            price,
            total
        ))

        self.conn.commit()

    def reduce_stock(self, product_id, quantity):

        sql = """
        UPDATE inventory
        SET quantity = quantity - %s
        WHERE id = %s
        """

        self.cursor.execute(sql, (
            quantity,
            product_id
        ))

        self.conn.commit()

    def get_serial_numbers(self, product_id):

        print("Searching serials for product:", product_id)

        sql = """
        SELECT serial_number
        FROM serial_numbers
        WHERE product_id=%s
        AND status='In Stock'
        """

        self.cursor.execute(sql, (int(product_id),))

        result = self.cursor.fetchall()

        print("Serials found:", result)

        return result


    def sell_serial_number(self, serial_number):

        sql = """
        UPDATE serial_numbers
        SET status='Sold'
        WHERE serial_number=%s
        """

        self.cursor.execute(sql, (serial_number,))
        self.conn.commit()

# ==========================================
# DATABASE OBJECT
# ==========================================

db = Database()
db.create_tables()