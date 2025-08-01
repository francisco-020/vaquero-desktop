import customtkinter as ctk
from .home_feed import HomeFeedTab
from .post_listing import PostListingTab
from .bookmarks import BookmarksTab
from .listing_detail import ListingDetailTab

class MainDashboard(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", pady=(10, 0), padx=10)

        logout_button = ctk.CTkButton(
            top_bar,
            text="Logout",
            width=80,
            command=self.logout
        )
        logout_button.pack(side="right")

        
        self.tabs = ctk.CTkTabview(self, width=780, height=560)
        self.tabs.pack(padx=10, pady=(10, 10), expand=True)

        # Add tabs
        self.home_tab = self.tabs.add("Home")
        self.post_tab = self.tabs.add("Post")
        self.bookmarks_tab = self.tabs.add("Bookmarks")
        self.details_tab = self.tabs.add("Details")

        # Populate tabs
        HomeFeedTab(self.home_tab)
        PostListingTab(self.post_tab)
        BookmarksTab(self.bookmarks_tab)
        ListingDetailTab(self.details_tab)

    def logout(self):
        print("Logging out...")
        self.controller.show_frame("LoginWindow")
