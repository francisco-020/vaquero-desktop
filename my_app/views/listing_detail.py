import customtkinter as ctk
from tkinter import messagebox
from lib.supabase_Client import supabase
from PIL import Image, ImageTk
import requests
from io import BytesIO
from my_app.auth.session import get_user_id

# Tab for displaying and managing the current user's own listings.
# Provides options to edit, delete, and mark listings as sold/available.
class ListingDetailTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")

        # Title label
        ctk.CTkLabel(self, text="My Listings", font=("Arial", 16, "bold")).pack(pady=10)

        # Refresh button
        self.refresh_button = ctk.CTkButton(self,fg_color="#ec6f05",hover_color="#dc6600", text="Refresh My Listings", command=self.load_my_listings)
        self.refresh_button.pack(pady=10)

        # Scrollable frame to hold all listing cards
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=760, height=500)
        self.scrollable_frame.pack(pady=5)    

    # Fetches the current user's listings from Supabase and render them.
    def load_my_listings(self):
         
        user_id = get_user_id()

        if user_id is None:
            messagebox.showerror("Error", "No logged-in user found. Please log in first.")
            return

        # Fetch the user's listings from Supabase
        response = supabase.table("Listings").select("*").eq("user_id", user_id).execute()

        # Clear old listings before loading new ones
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        listings = response.data

        if not listings:
                ctk.CTkLabel(self.scrollable_frame, text="No listings available.").pack(pady=10)
                return
        
        # Render each listing card
        for listing in listings:
                self.render_listing(listing)

    # Renders one listing card with details and action buttons
    def render_listing(self, listing):

        container = ctk.CTkFrame(self.scrollable_frame, fg_color="#f9f9f9", corner_radius=10)
        container.pack(padx=10, pady=10, fill="x")

        # Extract listing details
        title = listing.get("title", "Untitled")
        desc = listing.get("description", "")
        price = listing.get("price", "N/A")
        location = listing.get("item_location", "")
        display_name = listing.get("display_name", "Anonymous")
        image_url = listing.get("image_url")
        sold = listing.get("sold", False)

        # Show listing details
        ctk.CTkLabel(container, text=title, font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
        ctk.CTkLabel(container, text=f"Posted by: {display_name}", font=("Arial", 11, "italic")).pack(anchor="w", padx=10)
        ctk.CTkLabel(container, text=f"${price} | {location}", font=("Arial", 12)).pack(anchor="w", padx=10)
        ctk.CTkLabel(container, text=desc, wraplength=700, font=("Arial", 12)).pack(anchor="w", padx=10, pady=(0, 5))
        ctk.CTkLabel(container, text="Status: Sold" if sold else "Status: Available", font=("Arial", 11)).pack(anchor="w", padx=10)
       
        # Image display
        if image_url:
            try:
                image = self.load_image_from_url(image_url)
                img_label = ctk.CTkLabel(container, image=image, text="")
                img_label.image = image  # Prevent garbage collection
                img_label.pack(padx=10, pady=10)
            except Exception as e:
                ctk.CTkLabel(container, text=f"Failed to load image: {e}").pack(padx=10, pady=(0, 10))
        
        # Button frame (edit, delete, toggle status)
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(pady=5)

        # Edit button
        ctk.CTkButton(btn_frame, text="Edit", fg_color="blue", command=lambda l=listing: self.edit_listing(l)).pack(side="left", padx=5)
        
        # Delete button
        ctk.CTkButton(btn_frame, text="Delete", fg_color="red", command=lambda l=listing: self.delete_listing(l["id"])).pack(side="left", padx=5)

        # Mark as sold/available button
        toggle_text = "Mark as Available" if sold else "Mark as Sold"
        ctk.CTkButton(btn_frame, text=toggle_text, fg_color="orange", command=lambda l=listing: self.toggle_sold(l["id"], not sold)).pack(side="left", padx=5)

    # Fetch an image from a URL and return a Tkinter compatible image
    def load_image_from_url(self, url):
        response = requests.get(url)
        img_data = response.content
        pil_image = Image.open(BytesIO(img_data))
        pil_image = pil_image.resize((300, 200)) 
        return ImageTk.PhotoImage(pil_image)

    # Permanently delete a listing after user confirmation
    def delete_listing(self, listing_id):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this listing?"):
            supabase.table("Listings").delete().eq("id", listing_id).execute()
            self.load_my_listings()

    # Toggle the sold status of a listing
    def toggle_sold(self, listing_id, new_status):
        supabase.table("Listings").update({"sold": new_status}).eq("id", listing_id).execute()
        self.load_my_listings()

    # Open a small popup window to edit title and price of a listing
    def edit_listing(self, listing):
        edit_win = ctk.CTkToplevel(self)
        edit_win.title("Edit Listing")

        # Title input
        title_entry = ctk.CTkEntry(edit_win, width=200)
        title_entry.insert(0, listing.get("title", ""))
        title_entry.pack(pady=5)

        # Price input
        price_entry = ctk.CTkEntry(edit_win, width=200)
        price_entry.insert(0, listing.get("price", ""))
        price_entry.pack(pady=5)

        # Save button
        def save_changes():
            supabase.table("Listings").update({
                "title": title_entry.get().strip(),
                "price": float(price_entry.get().strip())
            }).eq("id", listing["id"]).execute()
            edit_win.destroy()
            self.load_my_listings()

        ctk.CTkButton(edit_win, text="Save", fg_color="green", command=save_changes).pack(pady=10) 
