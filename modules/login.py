import customtkinter as ctk
from tkinter import messagebox


class LoginWindow:
    def __init__(self, root):
        self.root = root

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root.title("Maximum Computer Technologies ERP")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        title = ctk.CTkLabel(
            root,
            text="Maximum Computer Technologies ERP",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=30)

        slogan = ctk.CTkLabel(
            root,
            text="Technology is our pride",
            font=("Arial", 16)
        )
        slogan.pack(pady=5)

        self.username = ctk.CTkEntry(
            root,
            width=300,
            placeholder_text="Username"
        )
        self.username.pack(pady=15)

        self.password = ctk.CTkEntry(
            root,
            width=300,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=15)

        login_btn = ctk.CTkButton(
            root,
            text="LOGIN",
            width=300,
            command=self.login
        )
        login_btn.pack(pady=30)

    def login(self):
        if self.username.get() == "admin" and self.password.get() == "admin123":

            self.root.destroy()

            new_root = ctk.CTk()

            from modules.dashboard import Dashboard

            Dashboard(new_root)

            new_root.mainloop()

        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password"
            )  
            
    
