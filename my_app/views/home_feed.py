import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from lib.supabase_Client import supabase  # adjust if your path differs

class HomeFeedTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")

        label = ctk.CTkLabel(self, text="Home Feed (All Active Listings)", font=("Arial", 16, "bold"))
        label.pack(pady=10)

        # Add refresh button
        self.refresh_button = ctk.CTkButton(self, text="Refresh Listings", command=self.load_listings)
        self.refresh_button.pack(pady=5)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=760, height=500)
        self.scrollable_frame.pack(pady=10)

        self.load_listings()

    def load_listings(self):
        # Clear existing widgets first
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            response = supabase.table("Listings").select("*").eq("sold", False).order("created_at", desc=True).execute()
            listings = response.data

            if not listings:
                ctk.CTkLabel(self.scrollable_frame, text="No listings available.").pack(pady=10)
                return

            for listing in listings:
                self.render_listing(listing)

        except Exception as e:
            ctk.CTkLabel(self.scrollable_frame, text=f"Error loading listings: {e}").pack(pady=10)

    def render_listing(self, listing):
        container = ctk.CTkFrame(self.scrollable_frame, fg_color="#f9f9f9", corner_radius=10)
        container.pack(padx=10, pady=10, fill="x")

        title = listing.get("title", "Untitled")
        desc = listing.get("description", "")
        price = listing.get("price", "N/A")
        location = listing.get("item_location", "")
        display_name = listing.get("display_name", "Anonymous")
        image_url = listing.get("image_url")

        # Top info block
        ctk.CTkLabel(container, text=title, font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
        ctk.CTkLabel(container, text=f"Posted by: {display_name}", font=("Arial", 11, "italic")).pack(anchor="w", padx=10)
        ctk.CTkLabel(container, text=f"${price} | {location}", font=("Arial", 12)).pack(anchor="w", padx=10)
        ctk.CTkLabel(container, text=desc, wraplength=700, font=("Arial", 12)).pack(anchor="w", padx=10, pady=(0, 5))

        # Image display
        if image_url:
            try:
                image = self.load_image_from_url(image_url)
                img_label = ctk.CTkLabel(container, image=image, text="")
                img_label.image = image  # Prevent garbage collection
                img_label.pack(padx=10, pady=10)
            except Exception as e:
                ctk.CTkLabel(container, text=f"Failed to load image: {e}").pack(padx=10, pady=(0, 10))

    def load_image_from_url(self, url):
        response = requests.get(url)
        img_data = response.content
        pil_image = Image.open(BytesIO(img_data))
        pil_image = pil_image.resize((300, 200))  # resize as needed
        return ImageTk.PhotoImage(pil_image)
