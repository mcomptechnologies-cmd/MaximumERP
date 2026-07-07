from tkinter import ttk
from database.database import db
from tkinter import messagebox
import customtkinter as ctk


class Inventory:
    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        title = ctk.CTkLabel(
            self.frame,
            text="Inventory Management",
            font=("Arial", 24, "bold")
        )
        columns = (
            "ID",
            "Product",
            "Category",
            "Qty",
            "Buying",
            "Selling"
        )

        self.table = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings",
            height=10
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=120)

        title.pack(pady=20)

        self.table.pack(fill="x", padx=20, pady=10)
        self.load_products()
        self.table.bind("<<TreeviewSelect>>", self.select_product)
        self.product = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Product Name"
        )
        self.product.pack(pady=10)

        self.category = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Category"
        )
        self.category.pack(pady=10)

        self.quantity = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Quantity"
        )
        self.quantity.pack(pady=10)

        self.buying = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Buying Price"
        )
        self.buying.pack(pady=10)

        self.selling = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Selling Price"
        )
        self.selling.pack(pady=10)

        add_btn = ctk.CTkButton(
            self.frame,
            text="Add Product",
            command=self.add_product
        )
        add_btn.pack(pady=20)
    def load_products(self):

        for row in self.table.get_children():
            self.table.delete(row)

        products = db.get_products()

        for product in products:

            self.table.insert(
                "",
                "end",
                values=(
                    product["id"],
                    product["product_name"],
                    product["category"],
                    product["quantity"],
                    product["buying_price"],
                    product["selling_price"]
                )
            )
    def add_product(self):
        try:
            db.add_product(
                self.product.get(),
                self.category.get(),
                int(self.quantity.get()),
                float(self.buying.get()),
                float(self.selling.get())
            )

            messagebox.showinfo(
                "Success",
                "Product saved successfully!"
            )
            self.load_products()
    def select_product(self, event):

        selected = self.table.focus()

        if not selected:
            return

        values = self.table.item(selected)["values"]

        self.selected_id = values[0]

        self.product.delete(0, "end")
        self.product.insert(0, values[1])

        self.category.delete(0, "end")
        self.category.insert(0, values[2])

        self.quantity.delete(0, "end")
        self.quantity.insert(0, values[3])

        self.buying.delete(0, "end")
        self.buying.insert(0, values[4])

        self.selling.delete(0, "end")
        self.selling.insert(0, values[5])
            self.product.delete(0, "end")
            self.category.delete(0, "end")
            self.quantity.delete(0, "end")
            self.buying.delete(0, "end")
            self.selling.delete(0, "end")

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
    def load_products(self):

        # Clear table
        for row in self.table.get_children():
            self.table.delete(row)

        # Load from database
        products = db.get_products()

        for product in products:
            self.table.insert(
                "",
                "end",
                values=(
                    product["id"],
                    product["product_name"],
                    product["category"],
                    product["quantity"],
                    product["buying_price"],
                    product["selling_price"]
                )
            )