import customtkinter as ctk
from modules.inventory import Inventory


class Dashboard:

    def __init__(self, root):

        self.root = root
        self.root.title("Maximum Computer Technologies ERP")
        self.root.geometry("1300x750")

        # ---------------- Header ----------------
        self.header = ctk.CTkFrame(self.root, height=70)
        self.header.pack(fill="x")

        title = ctk.CTkLabel(
            self.header,
            text="Maximum Computer Technologies ERP",
            font=("Arial", 24, "bold")
        )

        title.pack(side="left", padx=20, pady=20)

        user = ctk.CTkLabel(
            self.header,
            text="Logged in: Administrator",
            font=("Arial", 16)
        )

        user.pack(side="right", padx=20)

        # ---------------- Main ----------------
        self.main = ctk.CTkFrame(self.root)
        self.main.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main, width=220)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        # Content Area
        self.content = ctk.CTkFrame(self.main)
        self.content.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Sidebar Buttons
        ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            command=self.show_dashboard
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="Inventory",
            command=self.show_inventory
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="Sales"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="Customers"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="Repairs"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="Reports"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="Settings"
        ).pack(fill="x", padx=10, pady=5)

        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        cards = ctk.CTkFrame(self.content)
        cards.pack()

        stats = [
            ("Inventory", "0"),
            ("Customers", "0"),
            ("Sales", "KES 0"),
            ("Repairs", "0")
        ]

        for title, value in stats:

            card = ctk.CTkFrame(cards, width=180, height=120)
            card.pack(side="left", padx=10)

            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 18)
            ).pack(pady=10)

            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial", 24, "bold")
            ).pack()

    def show_inventory(self):

        self.clear_content()

        page = Inventory(self.content)

        page.frame.pack(fill="both", expand=True)