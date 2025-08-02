import customtkinter as ctk
from .home_feed import HomeFeedTab
from .post_listing import PostListingTab
from .bookmarks import BookmarksTab
from .listing_detail import ListingDetailTab

class MainDashboard(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.configure(fg_color="white")

        top_frame = ctk.CTkFrame(self, fg_color="#ec6f05", height=60)
        top_frame.pack(fill="x", side="top")

        ctk.CTkLabel(top_frame, text="🟧 Vaquero Marketplace",
                           font=("Georgia", 20, "bold")).pack(side="left", padx=10)

        ctk.CTkEntry(top_frame, placeholder_text="Search", width=300).pack(side="left", padx=20)



        ctk.CTkButton(top_frame, text="Log Off", width=60, fg_color="white",
                                text_color="black", command=self.logout).pack(side="right", padx=10)

        # Navigation
        top_bar = ctk.CTkFrame(self, fg_color="white", height=60)
        top_bar.pack(fill="x", pady=10)
        
        self.tabs = ctk.CTkTabview(top_bar, width=120, fg_color="#ec6f05", text_color="black")
        self.tabs.pack(padx=10, pady=(10, 10), expand=True)

        # Add tabs
        self.home_tab = self.tabs.add("🏠 Home Feed")
        self.details_tab = self.tabs.add("👤My Dashboard")
        self.bookmarks_tab = self.tabs.add("🖤 Bookmarked")
        self.post_tab = self.tabs.add("➕ Add Listing")
       
       

        # Populate tabs
        HomeFeedTab(self.home_tab)
        PostListingTab(self.post_tab)
        BookmarksTab(self.bookmarks_tab)
        ListingDetailTab(self.details_tab)

    def logout(self):
        print("Logging out...")
        self.controller.show_frame("LoginWindow")
