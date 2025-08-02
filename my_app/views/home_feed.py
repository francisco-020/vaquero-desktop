import customtkinter as ctk

class HomeFeedTab:
    def __init__(self, parent):
        label = ctk.CTkLabel(parent, text="Home Feed (Published Listings will show here)", font=("Arial", 16))
        label.pack(pady=20)
