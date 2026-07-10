import customtkinter as ctk
from tkinter import ttk, messagebox
from database.database import db


class Inventory:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.selected_id = None

        title = ctk.CTkLabel(
            self.frame,
            text="Inventory Management",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=10)

        # ---------------- Form ----------------

        form = ctk.CTkFrame(self.frame)
        form.pack(fill="x", padx=10, pady=10)

        self.product = ctk.CTkEntry(
            form,
            placeholder_text="Product Name",
            width=250
        )
        self.product.grid(row=0, column=0, padx=5, pady=5)

        self.category = ctk.CTkEntry(
            form,
            placeholder_text="Category",
            width=250
        )
        self.category.grid(row=0, column=1, padx=5, pady=5)

        self.quantity = ctk.CTkEntry(
            form,
            placeholder_text="Quantity",
            width=250
        )
        self.quantity.grid(row=1, column=0, padx=5, pady=5)

        self.buying = ctk.CTkEntry(
            form,
            placeholder_text="Buying Price",
            width=250
        )
        self.buying.grid(row=1, column=1, padx=5, pady=5)

        self.selling = ctk.CTkEntry(
            form,
            placeholder_text="Selling Price",
            width=250
        )
        self.selling.grid(row=2, column=0, padx=5, pady=5)

        # ---------------- Buttons ----------------

        button_frame = ctk.CTkFrame(self.frame)
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Add",
            width=120,
            command=self.add_product
        ).grid(row=0, column=0, padx=5)

        ctk.CTkButton(
            button_frame,
            text="Update",
            width=120,
            command=self.update_product
        ).grid(row=0, column=1, padx=5)

        ctk.CTkButton(
            button_frame,
            text="Delete",
            width=120,
            fg_color="red",
            command=self.delete_product
        ).grid(row=0, column=2, padx=5)

        ctk.CTkButton(
            button_frame,
            text="Clear",
            width=120,
            command=self.clear_entries
        ).grid(row=0, column=3, padx=5)

        # ---------------- Table ----------------

        columns = (
            "ID",
            "Product",
            "Category",
            "Quantity",
            "Buying",
            "Selling"
        )

        self.table = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings",
            height=12
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=120, anchor="center")

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.table.bind(
            "<<TreeviewSelect>>",
            self.select_product
        )

        self.load_products()
            # =====================================================
    # Load Products
    # =====================================================

    def load_products(self):

        # Clear existing rows
        for row in self.table.get_children():
            self.table.delete(row)

        # Load products from database
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

    # =====================================================
    # Clear Form
    # =====================================================

    def clear_entries(self):

        self.selected_id = None

        self.product.delete(0, "end")
        self.category.delete(0, "end")
        self.quantity.delete(0, "end")
        self.buying.delete(0, "end")
        self.selling.delete(0, "end")

    # =====================================================
    # Select Product
    # =====================================================

    def select_product(self, event=None):

        selected = self.table.focus()

        if not selected:
            return

        values = self.table.item(selected)["values"]

        if not values:
            return

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

        print("Selected ID:", self.selected_id)
            # =====================================================
    # Add Product
    # =====================================================

    def add_product(self):

        # Validation
        if (
            not self.product.get().strip() or
            not self.category.get().strip() or
            not self.quantity.get().strip() or
            not self.buying.get().strip() or
            not self.selling.get().strip()
        ):
            messagebox.showwarning(
                "Validation",
                "Please fill in all fields."
            )
            return

        try:

            quantity = int(self.quantity.get())
            buying = float(self.buying.get())
            selling = float(self.selling.get())

            db.add_product(
                self.product.get().strip(),
                self.category.get().strip(),
                quantity,
                buying,
                selling
            )

            messagebox.showinfo(
                "Success",
                "Product added successfully."
            )

            self.load_products()
            self.clear_entries()

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Quantity must be an integer.\nBuying and Selling prices must be numbers."
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================================
    # Update Product
    # =====================================================

    def update_product(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Update",
                "Please select a product first."
            )
            return

        try:

            quantity = int(self.quantity.get())
            buying = float(self.buying.get())
            selling = float(self.selling.get())

            db.update_product(
                self.selected_id,
                self.product.get().strip(),
                self.category.get().strip(),
                quantity,
                buying,
                selling
            )

            messagebox.showinfo(
                "Success",
                "Product updated successfully."
            )

            self.load_products()
            self.clear_entries()

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Quantity must be an integer.\nBuying and Selling prices must be numbers."
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =====================================================
    # Delete Product
    # =====================================================

    def delete_product(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Delete",
                "Please select a product first."
            )
            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this product?"
        )

        if not answer:
            return

        try:

            db.delete_product(self.selected_id)

            messagebox.showinfo(
                "Success",
                "Product deleted successfully."
            )

            self.load_products()
            self.clear_entries()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )