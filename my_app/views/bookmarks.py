import customtkinter as ctk
from tkinter import messagebox
from my_app.auth.session import get_user_id
from lib.supabase_Client import supabase  

# A tab (frame) that displays the user's bookmarked listings
# Allows refreshing, viewing, and removing bookmarks
class BookmarksTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,fg_color="white")

        # Title label
        label = ctk.CTkLabel(self, text="Bookmarks Page", font=("Arial", 16,"bold"))
        label.pack(pady=10)

        # Refresh button
        self.refresh_button = ctk.CTkButton(self,fg_color="#ec6f05",hover_color="#dc6600", text="Refresh Bookmarks", command=self.load_bookmarks)
        self.refresh_button.pack(pady=10)

        # Scrollable area to display bookmarked listings
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=760, height=500)
        self.scrollable_frame.pack(pady=5)


    # Fetches and displays the user's bookmarked listings
    def load_bookmarks(self):

        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Makes sure user is logged in
        user_id = get_user_id()
        if not user_id:
            messagebox.showerror("Error", "You must be logged in to view bookmarks.")
            return

        try:
            #Get the listing IDs the user has bookmarked
            bookmarks_resp = supabase.table("Bookmarks").select("listing_id").eq("user_id", user_id).execute()
            bookmark_ids = [b["listing_id"] for b in bookmarks_resp.data]

            if not bookmark_ids:
                ctk.CTkLabel(self.scrollable_frame, text="You have no bookmarks yet.").pack(pady=10)
                return

            # Fetch listing details for those IDs
            listings_resp = supabase.table("Listings").select("*").in_("id", bookmark_ids).execute()
            listings = listings_resp.data

            if not listings:
                ctk.CTkLabel(self.scrollable_frame, text="No listings found for your bookmarks.").pack(pady=10)
                return
            
            # Render each bookmarked listing
            for listing in listings:
                self.render_listing(listing)

        except Exception as e:
            ctk.CTkLabel(self.scrollable_frame, text=f"Error loading bookmarks: {e}").pack(pady=10)

    # Renders a single bookmarked listing inside the scrollable frame.
    def render_listing(self, listing):
        
        # Container for one listing
        container = ctk.CTkFrame(self.scrollable_frame, fg_color="#f9f9f9", corner_radius=10)
        container.pack(padx=10, pady=10, fill="x")

        # Extract listing fields
        title = listing.get("title", "Untitled")
        desc = listing.get("description", "")
        price = listing.get("price", "N/A")
        location = listing.get("item_location", "")
        display_name = listing.get("display_name", "Anonymous")
        image_url = listing.get("image_url")


        # Show listing details
        ctk.CTkLabel(container, text=title, font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
        ctk.CTkLabel(container, text=f"Posted by: {display_name}", font=("Arial", 11, "italic")).pack(anchor="w", padx=10)
        ctk.CTkLabel(container, text=f"${price} | {location}", font=("Arial", 12)).pack(anchor="w", padx=10)
        ctk.CTkLabel(container, text=desc, wraplength=700, font=("Arial", 12)).pack(anchor="w", padx=10, pady=(0, 5))


        # Remove from bookmarks button
        remove_btn = ctk.CTkButton(container, text="Remove from Bookmarks", fg_color="#d9534f", hover_color="#c9302c", command=lambda: self.remove_bookmark(listing["id"], container))  # Pass container to remove UI
        remove_btn.pack(anchor="e", padx=10, pady=(0, 8))

    # Deletes a bookmark from the database and remove it from UI.
    def remove_bookmark(self, listing_id, container):
        user_id = get_user_id()
        if not user_id:
            messagebox.showerror("Error", "You must be logged in to remove bookmarks.")
            return

        try:
            # Delete bookmark record from Supabase
            supabase.table("Bookmarks") \
                .delete() \
                .eq("user_id", user_id) \
                .eq("listing_id", listing_id) \
                .execute()

            container.destroy()  # Removes the card from UI
            messagebox.showinfo("Removed", "Bookmark removed successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Could not remove bookmark: {e}")

