import customtkinter as ctk
from .home_feed import HomeFeedTab
from .post_listing import PostListingTab
from .bookmarks import BookmarksTab
from .listing_detail import ListingDetailTab
from PIL import Image
from tkinter import messagebox
import requests
import os
from lib.supabase_Client import supabase
from my_app.auth.session import get_user_id

# Main dashboard frame that contains navigation, header, and page views (home feed, my listings, bookmarks, and add listing).
class MainDashboard(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.configure(fg_color="white")

        # Load logo for header
        logo_image = ctk.CTkImage(light_image=Image.open("images/UTRGV Logo.png"), size=(32, 32))

        # Top Header (Logo, Delete Account, Log Off)
        top_frame = ctk.CTkFrame(self, fg_color="#ec6f05", height=70)
        top_frame.pack(fill="x", side="top")

        # App name and logo
        ctk.CTkLabel(top_frame, image=logo_image, text=" Vaquero Marketplace", text_color="white", font=("Georgia", 20, "bold"), compound="left").pack(side="left", padx=20, pady=30)

        # Log off button
        ctk.CTkButton(top_frame, text="Log Off", width=70, fg_color="white", hover_color="#d95e00", text_color="black", command=self.logout).pack(side="right", padx=30, pady=30)

        # Delete account button
        ctk.CTkButton(top_frame, text="Delete Account", width=120, fg_color="red", hover_color="#b30000",text_color="white", command=self.delete_account).pack(side="right", padx=(0, 10), pady=30)

        # Navigation Menu (buttons to switch pages)
        nav_frame = ctk.CTkFrame(self, fg_color="white", height=50)
        nav_frame.pack(fill="x", pady=(5, 20))

        self.nav_buttons = {}
        nav_items = [
            ("Home Feed", "home"),
            ("My Dashboard", "dashboard"),
            ("Bookmarked", "bookmarks"),
            ("Add Listing", "add")
        ]

        # Create navigation buttons dynamically
        for text, key in nav_items:
            btn = ctk.CTkButton(nav_frame, text=text, width=130, height=35, fg_color="transparent", hover_color="#d95e00", text_color="black", command=lambda k=key: self.show_page(k))
            btn.pack(side="left", padx=10)
            self.nav_buttons[key] = btn

        # Page content Area
        self.pages = {
            "home": HomeFeedTab(self),
            "dashboard": ListingDetailTab(self),
            "bookmarks": BookmarksTab(self),
            "add": PostListingTab(self)
        }

        # Show only the home page at start
        for page in self.pages.values():
            page.pack_forget()
        self.pages["home"].pack(fill="both", expand=True)
        self.highlight_nav("home")

    # Hide all pages and show the selected one
    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack(fill="both", expand=True)
        self.highlight_nav(page_name)

    # Highlight the active nav button
    def highlight_nav(self, active_key):
        for key, btn in self.nav_buttons.items():
            btn.configure(fg_color="transparent", text_color="black")
        self.nav_buttons[active_key].configure(fg_color="#d95e00", text_color="white")

    # Log the user out by switching back to login
    def logout(self):
        print("Logging out...")
        self.controller.show_frame("LoginWindow")

    # Permanently delete the user's account from Supabase Auth and redirect to login screen.
    def delete_account(self):

        user_id = get_user_id()
        if not user_id:
            messagebox.showerror("Error", "You must be logged in to delete your account.")
            return

        # Ask user for confirmation
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete your account? This cannot be undone."
        )
        if not confirm:
            return

        try:
            # Delete from Supabase Auth
            service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            url = f"{os.getenv('SUPABASE_URL')}/auth/v1/admin/users/{user_id}"

            headers = {
                "apikey": service_role_key,
                "Authorization": f"Bearer {service_role_key}",
                "Content-Type": "application/json"
            }
            
            # Send delete request
            response = requests.delete(url, headers=headers)

            # Handle response
            if response.status_code == 204:
                messagebox.showinfo("Deleted", "Your account has been permanently deleted.")
                self.controller.show_frame("LoginWindow")
                return
            elif 200 <= response.status_code < 300:
                messagebox.showinfo("Deleted", "Your account has been deleted.")
                self.controller.show_frame("LoginWindow")
                return
            else:
                messagebox.showerror(
                    "Error",
                    f"Failed to delete account: {response.status_code} - {response.text}"
                )


        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
