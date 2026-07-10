import customtkinter as ctk
from tkinter import ttk
from database.database import db


class Sales:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            self.frame,
            text="Sales Management",
            font=("Arial", 24, "bold")
        ).pack(pady=10)

        # Customer Name
        self.customer = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Customer Name"
        )
        self.customer.pack(pady=5)

        # Search Product
        self.search = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Search Product"
        )
        self.search.pack(pady=5)

        # Quantity
        self.quantity = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Quantity"
        )
        self.quantity.pack(pady=5)

        # Buttons
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Add To Cart"
        ).grid(row=0, column=0, padx=5)

        ctk.CTkButton(
            button_frame,
            text="Complete Sale"
        ).grid(row=0, column=1, padx=5)

        # Product Table
        columns = (
            "ID",
            "Product",
            "Category",
            "Stock",
            "Price"
        )

        self.products = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings",
            height=10
        )

        for col in columns:
            self.products.heading(col, text=col)
            self.products.column(col, width=130, anchor="center")

        self.products.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_products()

    def load_products(self):

        for row in self.products.get_children():
            self.products.delete(row)

        products = db.get_products()

        for product in products:

            self.products.insert(
                "",
                "end",
                values=(
                    product["id"],
                    product["product_name"],
                    product["category"],
                    product["quantity"],
                    product["selling_price"]
                )
            )