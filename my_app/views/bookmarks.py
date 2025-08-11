import customtkinter as ctk
from tkinter import messagebox
from my_app.auth.session import get_user_id
from lib.supabase_Client import supabase  # adjust if your path differs



class BookmarksTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,fg_color="white")

        label = ctk.CTkLabel(self, text="Bookmarks Page", font=("Arial", 16,"bold"))
        label.pack(pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=760, height=500)
        self.scrollable_frame.pack(pady=10)

        
    def load_bookmarks(self):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        user_id = get_user_id()
        if not user_id:
            messagebox.showerror("Error", "You must be logged in to view bookmarks.")
            return

        try:
            # Get bookmarked listing ids
            bookmarks_resp = supabase.table("Bookmarks").select("listing_id").eq("user_id", user_id).execute()
            bookmark_ids = [b["listing_id"] for b in bookmarks_resp.data]

            if not bookmark_ids:
                ctk.CTkLabel(self.scrollable_frame, text="You have no bookmarks yet.").pack(pady=10)
                return

            # Fetch listings for those ids
            listings_resp = supabase.table("Listings").select("*").in_("id", bookmark_ids).execute()
            listings = listings_resp.data

            if not listings:
                ctk.CTkLabel(self.scrollable_frame, text="No listings found for your bookmarks.").pack(pady=10)
                return

            for listing in listings:
                self.render_listing(listing)

        except Exception as e:
            ctk.CTkLabel(self.scrollable_frame, text=f"Error loading bookmarks: {e}").pack(pady=10)

    def render_listing(self, listing):
        container = ctk.CTkFrame(self.scrollable_frame, fg_color="#f9f9f9", corner_radius=10)
        container.pack(padx=10, pady=10, fill="x")

        title = listing.get("title", "Untitled")
        price = listing.get("price", "N/A")
        location = listing.get("item_location", "")

        ctk.CTkLabel(container, text=f"{title} - ${price} ({location})", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(5, 0))