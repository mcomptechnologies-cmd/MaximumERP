import customtkinter as ctk
from modules.login import LoginWindow

ctk.set_appearance_mode("light")

root = ctk.CTk()

LoginWindow(root)

root.mainloop()