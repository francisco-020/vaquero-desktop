import customtkinter as ctk

class BookmarksTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,fg_color="white")

        label = ctk.CTkLabel(self, text="Bookmarks Page (Coming Soon)", font=("Arial", 16,"bold"))
        label.pack(pady=20)
