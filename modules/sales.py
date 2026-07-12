import customtkinter as ctk
from tkinter import ttk, messagebox
from database.database import db
from datetime import datetime


class Sales:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Temporary shopping cart
        self.cart = []

        self.selected_product = None

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
            text="Add To Cart",
            command=self.add_to_cart
        ).grid(row=0, column=0, padx=5)

        ctk.CTkButton(
            button_frame,
            text="Complete Sale",
            command=self.complete_sale
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

        self.products.bind(
            "<<TreeviewSelect>>",
            self.select_product
       )
        
        self.load_products()

        # =====================================================
        # Shopping Cart
        # =====================================================

        cart_label = ctk.CTkLabel(
            self.frame,
            text="Shopping Cart",
            font=("Arial", 18, "bold")
        )
        cart_label.pack(pady=(10, 5))

        cart_columns = (
            "ID",
            "Product",
            "Qty",
            "Price",
            "Total"
        )

        self.cart_table = ttk.Treeview(
            self.frame,
            columns=cart_columns,
            show="headings",
            height=6
        )

        for col in cart_columns:
            self.cart_table.heading(col, text=col)
            self.cart_table.column(col, width=120, anchor="center")

        self.cart_table.pack(fill="x", padx=10, pady=10)

        # Grand Total
        self.total_label = ctk.CTkLabel(
            self.frame,
            text="Grand Total: KES 0.00",
            font=("Arial", 18, "bold")
        )
        self.total_label.pack(pady=10)

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

    # =====================================================
    # Select Product
    # =====================================================

    def select_product(self, event=None):

        selected = self.products.focus()

        if not selected:
            return

        values = self.products.item(selected)["values"]

        if not values:
            return

        self.selected_product = values

        print("Selected:", values)

    # =====================================================
    # Add Product To Cart
    # =====================================================

    def add_to_cart(self):

        if self.selected_product is None:
            return

        try:
            qty = int(self.quantity.get())

            if qty <= 0:
                return

            product_id = self.selected_product[0]
            product_name = self.selected_product[1]
            stock = int(self.selected_product[3])
            price = float(self.selected_product[4])

            if qty > stock:
                print("Not enough stock")
                return
            serials = db.get_serial_numbers(product_id)

            if len(serials) < qty:
                print("Not enough serial numbers available.")
                return

            selected_serials = [
                s["serial_number"] for s in serials[:qty]
            ]
            
            total = qty * price

            self.cart.append({
                "product_id": product_id,
                "product_name": product_name,
                "quantity": qty,
                "price": price,
                "total": total,
                "serials": selected_serials
          })

            self.cart_table.insert(
                "",
                "end",
                values=(
                    product_id,
                    product_name,
                    qty,
                    f"{price:.2f}",
                    f"{total:.2f}"
                )
            )

            self.update_total()

            print("Added to cart")

        except ValueError:
            print("Invalid quantity")

    # =====================================================
    # Update Grand Total
    # =====================================================

    def update_total(self):

        total = sum(item["total"] for item in self.cart)

        self.total_label.configure(
            text=f"Grand Total: KES {total:,.2f}"
        )

    # =====================================================
    # Complete Sale
    # =====================================================

    def complete_sale(self):

        if not self.cart:
            messagebox.showwarning(
                "No Items",
                "Shopping cart is empty."
            )
            return

        customer = self.customer.get().strip()

        if customer == "":
            messagebox.showwarning(
                "Customer",
                "Enter customer name."
            )
            return

        invoice_no = datetime.now().strftime("INV%Y%m%d%H%M%S")

        grand_total = sum(item["total"] for item in self.cart)

        try:

            sale_id = db.save_sale(
                invoice_no,
                customer,
                grand_total
            )

            for item in self.cart:

                db.save_sale_item(
                    sale_id,
                    item["product_id"],
                    item["product_name"],
                    item["quantity"],
                    item["price"],
                    item["total"]
                )

                db.reduce_stock(
                    item["product_id"],
                    item["quantity"]
                )

                for serial in item["serials"]:
                    db.sell_serial_number(serial)

            messagebox.showinfo(
                "Success",
                f"Sale completed.\nInvoice: {invoice_no}"
            )

            self.cart.clear()

            for row in self.cart_table.get_children():
                self.cart_table.delete(row)

            self.update_total()

            self.customer.delete(0, "end")
            self.quantity.delete(0, "end")

            self.load_products()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )