import os
from supabase import create_client
from lib.supabase_Client import supabase
from upload_image import upload_file_to_storage
import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime


class PostListingTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")

        self.label = ctk.CTkLabel(self, text="Post a New Listing", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        self.title_entry = ctk.CTkEntry(self, placeholder_text="Title")
        self.title_entry.pack(pady=5)

        self.description_entry = ctk.CTkEntry(self, placeholder_text="Description")
        self.description_entry.pack(pady=5)

        self.price_entry = ctk.CTkEntry(self, placeholder_text="Price")
        self.price_entry.pack(pady=5)

        self.category_entry = ctk.CTkEntry(self, placeholder_text="Category")
        self.category_entry.pack(pady=5)

        self.location_entry = ctk.CTkEntry(self, placeholder_text="Location")
        self.location_entry.pack(pady=5)

        self.image_path = None

        self.select_image_btn = ctk.CTkButton(self, text="Select Image", command=self.select_image)
        self.select_image_btn.pack(pady=5)

        self.submit_btn = ctk.CTkButton(self, text="Post Listing", command=self.post_listing)
        self.submit_btn.pack(pady=15)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            self.image_path = file_path
            print("Selected image:", file_path)
            self.select_image_btn.configure(text=os.path.basename(file_path))

    def post_listing(self):
        session = supabase.auth.get_session()
        user = session.user if session else None

        if not user:
            print("User not logged in.")
            return

        user_id = user.id
        display_name = user.user_metadata.get("full_name") or user.email or "Anonymous"

        access_token = session.access_token

        image_url = ""
        if self.image_path:
            image_name = os.path.basename(self.image_path)
            image_url = upload_file_to_storage(self.image_path, image_name, access_token)
            if image_url is None:
                print("Failed to upload image. Aborting listing.")
                return
            print("Uploaded image URL:", image_url)

        try:
            price_value = self.price_entry.get().strip()
            if not price_value:
                print("Price is empty.")
                return

            listing = {
                "user_id": str(user_id),
                "display_name": str(display_name),
                "title": self.title_entry.get().strip(),
                "description": self.description_entry.get().strip(),
                "price": float(price_value),
                "category": self.category_entry.get().strip(),
                "image_url": image_url,
                "item_location": self.location_entry.get().strip(),
                "sold": False,
                "created_at": datetime.now().isoformat(),
            }

            print("Listing payload:", listing)

            response = supabase.table("Listings").insert(listing).execute()
            print("Supabase response:", response)

            if response.data:
                print("✅ Listing posted successfully.")
                messagebox.showinfo("Success", "Listing posted successfully!")

                # Clear form
                self.title_entry.delete(0, 'end')
                self.description_entry.delete(0, 'end')
                self.price_entry.delete(0, 'end')
                self.category_entry.delete(0, 'end')
                self.location_entry.delete(0, 'end')
                self.image_path = None
                self.select_image_btn.configure(text="Select Image")
            else:
                print("Error posting listing:", response.error)

        except Exception as e:
            print("Exception while posting listing:", e)
