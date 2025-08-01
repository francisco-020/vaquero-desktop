import customtkinter as ctk
from tkinter import messagebox
from lib.supabase_Client import supabase


class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.configure(fg_color="white")


        sidebar = ctk.CTkFrame(self, width=80, height=1000, fg_color="#ec6f05", corner_radius=0)
        sidebar.place(relx=1.0, rely=0, anchor="ne")

        self.top_title = ctk.CTkLabel(self, text="Welcome to Vaquero Marketplace", text_color="#ec6f05", font=("Georgia", 30, "bold")).pack( padx=25, pady=70)
        
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=25)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        
        self.login_button = ctk.CTkButton(self, text="Log In", width=200,
                            fg_color="#ec6f05", hover_color="#d95e00",
                            border_color="black", border_width=1,
                            command=self.login).pack(pady=15)

        self.signup_button = ctk.CTkButton(self, text="Create new account", width=200,
                            fg_color="white", text_color="black",
                            border_color="black", border_width=1,
                            command=self.login).pack(pady=10)
        
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
