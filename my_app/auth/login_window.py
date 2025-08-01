import customtkinter as ctk
from tkinter import messagebox
from lib.supabase_Client import supabase


class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.title_label = ctk.CTkLabel(self, text="Login to Vaquero Marketplace", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=20)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.signup_button = ctk.CTkButton(self, text="Sign Up", command=self.signup)
        self.signup_button.pack(pady=5)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if response.user:
                messagebox.showinfo("Login Success", f"Welcome {email}!")
                self.controller.show_frame("Dashboard") 

            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")
        except Exception as e:
            messagebox.showerror("Login Error", str(e))

    def signup(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            if response.user:
                messagebox.showinfo("Sign Up Success", "Check your email to confirm your account.")
            else:
                messagebox.showerror("Sign Up Failed", "Unable to create account.")
        except Exception as e:
            messagebox.showerror("Sign Up Error", str(e))
