import customtkinter as ctk
from .home_feed import HomeFeedTab
from .post_listing import PostListingTab
from .bookmarks import BookmarksTab
from .listing_detail import ListingDetailTab
from PIL import Image


class MainDashboard(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.configure(fg_color="white")
        logo_image = ctk.CTkImage(light_image=Image.open("images/UTRGV Logo.png"), size=(32, 32))

        # Top Header (Logo, Search, Log Off)
        top_frame = ctk.CTkFrame(self, fg_color="#ec6f05", height=70)
        top_frame.pack(fill="x", side="top")

        ctk.CTkLabel(
            top_frame, image=logo_image, text=" Vaquero Marketplace",
            text_color="white", font=("Georgia", 20, "bold"), compound="left"
        ).pack(side="left", padx=20, pady=30)

        ctk.CTkEntry(top_frame, placeholder_text="Search", width=300).pack(side="left", padx=20, pady=30)

        ctk.CTkButton(
            top_frame, text="Log Off", width=70, fg_color="white", hover_color="#d95e00",
            text_color="black", command=self.logout
        ).pack(side="right", padx=30, pady=30)

        # Navigation Menu 
        nav_frame = ctk.CTkFrame(self, fg_color="white", height=50)
        nav_frame.pack(fill="x", pady=(5, 20))

        self.nav_buttons = {}
        nav_items = [
            ("🏠 Home Feed", "home"),
            ("👤 My Dashboard", "dashboard"),
            ("🖤 Bookmarked", "bookmarks"),
            ("➕ Add Listing", "add")
        ]

        for text, key in nav_items:
            btn = ctk.CTkButton(
                nav_frame, text=text, width=130, height=35,
                fg_color="transparent", hover_color="#d95e00", text_color="black",
                command=lambda k=key: self.show_page(k)
            )
            btn.pack(side="left", padx=10)
            self.nav_buttons[key] = btn

        # Main Content Area
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

    def show_page(self, page_name):
        """Hide all pages and show the selected one."""
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack(fill="both", expand=True)
        self.highlight_nav(page_name)

    def highlight_nav(self, active_key):
        """Highlight the active nav button."""
        for key, btn in self.nav_buttons.items():
            btn.configure(fg_color="transparent", text_color="black")
        self.nav_buttons[active_key].configure(fg_color="#d95e00", text_color="white")

    def logout(self):
        print("Logging out...")
        self.controller.show_frame("LoginWindow")
