import customtkinter as ctk


class InventoryPage:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)

        title = ctk.CTkLabel(
            self.frame,
            text="Inventory Management",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)

        form = ctk.CTkFrame(self.frame)
        form.pack(padx=20, pady=10)

        labels = [
            "Item Name",
            "Category",
            "Barcode",
            "Quantity",
            "Buying Price",
            "Selling Price"
        ]

        self.entries = {}

        for row, label in enumerate(labels):

            ctk.CTkLabel(form, text=label).grid(
                row=row,
                column=0,
                padx=10,
                pady=8,
                sticky="w"
            )

            entry = ctk.CTkEntry(form, width=250)
            entry.grid(row=row, column=1, padx=10)

            self.entries[label] = entry

        buttons = ctk.CTkFrame(self.frame)
        buttons.pack(pady=20)

        ctk.CTkButton(buttons, text="Save", width=120).grid(row=0, column=0, padx=5)
        ctk.CTkButton(buttons, text="Update", width=120).grid(row=0, column=1, padx=5)
        ctk.CTkButton(buttons, text="Delete", width=120).grid(row=0, column=2, padx=5)
        ctk.CTkButton(buttons, text="Clear", width=120).grid(row=0, column=3, padx=5)