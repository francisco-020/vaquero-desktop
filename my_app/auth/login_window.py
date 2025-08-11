import customtkinter as ctk
from tkinter import messagebox
import webbrowser
from lib.supabase_Client import supabase
from PIL import Image
from my_app.auth.session import set_user_id


class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.configure(fg_color="white")
        logo_image = ctk.CTkImage(light_image=Image.open("images/UTRGV Logo.png"), size=(32, 32))
        self.is_registering = False

        self.sidebar = ctk.CTkFrame(self, width=80, height=1000, fg_color="#ec6f05", corner_radius=0)
        self.sidebar.place(relx=1.0, rely=0, anchor="ne")

        self.top_title = ctk.CTkLabel(self,image=logo_image, text=" Welcome to Vaquero Marketplace",
                                      text_color="#ec6f05", font=("Georgia", 30, "bold"),compound="left")
        self.top_title.pack(padx=25, pady=70)

        # Shared form fields
        self.first_name_entry = ctk.CTkEntry(self, placeholder_text="First Name", width=175)
        self.last_name_entry = ctk.CTkEntry(self, placeholder_text="Last Name", width=175)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", width=175)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=175)

        # Buttons
        self.main_button = ctk.CTkButton(self, text="Log In", width=200,
                                         fg_color="#ec6f05", hover_color="#dc6600",
                                         border_color="black", border_width=2,
                                         command=self.login_or_register)

        self.switch_button = ctk.CTkButton(self, text="Create New Account", width=200,
                                           fg_color="white", text_color="black",
                                           border_color="black", border_width=2,hover_color="#dc6600",
                                           command=self.toggle_form)

        self.google_button = ctk.CTkButton(self, text="Continue with Google", width=200,
                                           fg_color="white", text_color="black",
                                           hover_color="#dc6600",border_color="black", border_width=2,
                                           command=self.google_sign_in)

        self.render_login_form()

    def render_login_form(self):
        self.clear_form()

        self.email_entry.pack(pady=25)
        self.password_entry.pack(pady=10)
        self.main_button.configure(text="Log In")
        self.main_button.pack(pady=15)
        self.google_button.pack(pady=5)
        self.switch_button.configure(text="Create new account")
        self.switch_button.pack(pady=10)

        self.is_registering = False

    def render_register_form(self):
        self.clear_form()

        self.first_name_entry.pack(pady=5)
        self.last_name_entry.pack(pady=5)
        self.email_entry.pack(pady=10)
        self.password_entry.pack(pady=10)
        self.main_button.configure(text="Register")
        self.main_button.pack(pady=15)
        self.switch_button.configure(text="Back to Login")
        self.switch_button.pack(pady=10)

        
        self.is_registering = True

    def clear_form(self):
        for widget in [self.first_name_entry, self.last_name_entry,
                       self.email_entry, self.password_entry,
                       self.main_button, self.switch_button, self.google_button]:
            widget.pack_forget()

    def toggle_form(self):
        if self.is_registering:
            self.render_login_form()
        else:
            self.render_register_form()

    def login_or_register(self):
        if self.is_registering:
            self.register()
        else:
            self.login()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if response.user:
                set_user_id(response.user.id)  
                messagebox.showinfo("Login Success", f"Welcome {email}!")
                dashboard = self.controller.frames["Dashboard"]
                self.controller.show_frame("Dashboard")
                dashboard.pages["dashboard"].load_my_listings()
                dashboard.pages["bookmarks"].load_bookmarks()

            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")
        except Exception as e:
            messagebox.showerror("Login Error", str(e))

    def register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        first = self.first_name_entry.get()
        last = self.last_name_entry.get()

        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "first_name": first,
                        "last_name": last
                    }
                }
            })

            if response.user:
                messagebox.showinfo("Sign Up Success!")
                self.render_login_form()
            else:
                messagebox.showerror("Sign Up Failed", "Unable to create account.")
        except Exception as e:
            messagebox.showerror("Sign Up Error", str(e))

    def google_sign_in(self):
        url = "https://krsuokkfieczcaxmzisq.supabase.co/auth/v1/authorize?provider=google"
        webbrowser.open(url)

