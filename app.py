import customtkinter as ctk
from modules.login import LoginWindow

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()

LoginWindow(root)

root.mainloop()