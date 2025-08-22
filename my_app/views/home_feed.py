import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from lib.supabase_Client import supabase 
from my_app.auth.session import get_user_id
from tkinter import messagebox

# Tab (frame) that displays all active marketplace listings.
# Allows bookmarking of listings.
class HomeFeedTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")

        # Title label
        label = ctk.CTkLabel(self, text="Active Listings", font=("Arial", 16, "bold"))
        label.pack(pady=10)

        # Refresh button
        self.refresh_button = ctk.CTkButton(self,fg_color="#ec6f05",hover_color="#dc6600", text="Refresh Listings", command=self.load_listings)
        self.refresh_button.pack(pady=5)

        # Scrollable frame to hold all the listings
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=760, height=500)
        self.scrollable_frame.pack(pady=10)

        # Load listings immediately when the tab is opened
        self.load_listings()

    # Fetches all active listings from Supabase and renders them
    def load_listings(self):

        # Clear old listings
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            # Get all listings where sold = False, newest first
            response = supabase.table("Listings").select("*").eq("sold", False).order("created_at", desc=True).execute()
            listings = response.data

            if not listings:
                ctk.CTkLabel(self.scrollable_frame, text="No listings available.").pack(pady=10)
                return

            # Render each listing 
            for listing in listings:
                self.render_listing(listing)

        except Exception as e:
            ctk.CTkLabel(self.scrollable_frame, text=f"Error loading listings: {e}").pack(pady=10)

    # Renders one listing card inside the scrollable frame
    def render_listing(self, listing):

        # Container for a single listing
        container = ctk.CTkFrame(self.scrollable_frame, fg_color="#f9f9f9", corner_radius=10)
        container.pack(padx=10, pady=10, fill="x")

        # Extract listing details
        title = listing.get("title", "Untitled")
        desc = listing.get("description", "")
        price = listing.get("price", "N/A")
        location = listing.get("item_location", "")
        display_name = listing.get("display_name", "Anonymous")
        image_url = listing.get("image_url")

        # Display listing details
        ctk.CTkLabel(container, text=title, font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
        ctk.CTkLabel(container, text=f"Posted by: {display_name}", font=("Arial", 11, "italic")).pack(anchor="w", padx=10)
        ctk.CTkLabel(container, text=f"${price} | {location}", font=("Arial", 12)).pack(anchor="w", padx=10)
        ctk.CTkLabel(container, text=desc, wraplength=700, font=("Arial", 12)).pack(anchor="w", padx=10, pady=(0, 5))

        # Bookmark button
        ctk.CTkButton(container, text="Bookmark", command=lambda id=listing["id"]: self.add_bookmark(id)).pack(anchor="w", padx=10, pady=(0, 5))

        # Image display
        if image_url:
            try:
                image = self.load_image_from_url(image_url)
                img_label = ctk.CTkLabel(container, image=image, text="")
                img_label.image = image  # Prevent garbage collection
                img_label.pack(padx=10, pady=10)
            except Exception as e:
                ctk.CTkLabel(container, text=f"Failed to load image: {e}").pack(padx=10, pady=(0, 10))

    # Fetch an image from a URL and convert it into a Tkinter compatible image
    def load_image_from_url(self, url):
        response = requests.get(url)
        img_data = response.content
        pil_image = Image.open(BytesIO(img_data))
        pil_image = pil_image.resize((300, 200))
        return ImageTk.PhotoImage(pil_image)
        
    # Add a listing to the user's bookmarks in Supabase.
    def add_bookmark(self, listing_id):
        user_id = get_user_id()
        if not user_id:
            messagebox.showerror("Error", "You must be logged in to bookmark listings.")
            return

        try:
            # Inserts bookmark 
            response = supabase.table("Bookmarks").insert({
                "user_id": user_id,
                "listing_id": listing_id
            }).execute()

            if response.data:  # If insert was successful, there will be data
                messagebox.showinfo("Bookmarked", "Listing added to your bookmarks!")
            else:
                messagebox.showerror("Error", "Failed to add bookmark. It might already be bookmarked.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

