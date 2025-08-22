import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from lib.supabase_Client import supabase  
from my_app.auth.session import get_user_id
from tkinter import messagebox


class HomeFeedTab(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="white")

        # Title
        label = ctk.CTkLabel(self, text="Active Listings", font=("Arial", 16, "bold"))
        label.pack(pady=(10, 6))

        # Search / Filter bar
        self._build_search_bar()

        # Refresh button
        self.refresh_button = ctk.CTkButton(
            self,
            fg_color="#ec6f05",
            hover_color="#dc6600",
            text="Refresh Listings",
            command=self.reload  # now points to reload()
        )
        self.refresh_button.pack(pady=5)

        # Scrollable area
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=760, height=500)
        self.scrollable_frame.pack(pady=10, fill="both", expand=True)

        # Cache for all listings
        self.all_listings = []

        # Initial load
        self.reload()


    def _build_search_bar(self):

        self.query_var = ctk.StringVar()
        self.min_price_var = ctk.StringVar()
        self.max_price_var = ctk.StringVar()
        self.category_var = ctk.StringVar(value="All")

        bar = ctk.CTkFrame(self, fg_color="white")
        bar.pack(fill="x", padx=12, pady=(0, 8))

        ctk.CTkLabel(bar, text="Search").grid(row=0, column=0, padx=(0, 6), pady=6, sticky="w")
        search_entry = ctk.CTkEntry(bar, textvariable=self.query_var, placeholder_text="Title or description")
        search_entry.grid(row=0, column=1, padx=(0, 12), pady=6, sticky="ew")

        ctk.CTkLabel(bar, text="Category").grid(row=0, column=2, padx=(0, 6), pady=6, sticky="w")
        self.category_menu = ctk.CTkOptionMenu(bar, values=["All"], variable=self.category_var, width=140)
        self.category_menu.grid(row=0, column=3, padx=(0, 12), pady=6, sticky="w")

        ctk.CTkLabel(bar, text="Min $").grid(row=0, column=4, padx=(0, 6), pady=6, sticky="w")
        ctk.CTkEntry(bar, textvariable=self.min_price_var, width=90, placeholder_text="0").grid(row=0, column=5, padx=(0, 12), pady=6, sticky="w")

        ctk.CTkLabel(bar, text="Max $").grid(row=0, column=6, padx=(0, 6), pady=6, sticky="w")
        ctk.CTkEntry(bar, textvariable=self.max_price_var, width=90, placeholder_text="1000").grid(row=0, column=7, padx=(0, 12), pady=6, sticky="w")

        # Apply + Clear buttons
        ctk.CTkButton(bar, text="Apply", command=self.apply_filters, width=100).grid(row=0, column=8, padx=(0, 6), pady=6, sticky="e")
        ctk.CTkButton(bar, text="Clear", command=self.clear_filters, width=100).grid(row=0, column=9, padx=(0, 6), pady=6, sticky="e")

        bar.grid_columnconfigure(1, weight=1)

        # Live filtering while typing
        search_entry.bind("<KeyRelease>", lambda e: self.apply_filters())

    def reload(self):
        """Fetch all active (unsold) listings once, then filter in memory."""
        # Clear UI
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            # Pull everything we need (sold = False)
            response = supabase.table("Listings") \
                .select("*") \
                .eq("sold", False) \
                .order("created_at", desc=True) \
                .execute()

            self.all_listings = response.data or []

            # Populate category choices dynamically (if you use a 'category' field)
            cats = sorted({(it.get("category") or "").strip() for it in self.all_listings if it.get("category")})
            values = ["All"] + cats
            self.category_menu.configure(values=values)
            if self.category_var.get() not in values:
                self.category_var.set("All")

            # Apply current filters to render
            self.apply_filters()

        except Exception as e:
            ctk.CTkLabel(self.scrollable_frame, text=f"Error loading listings: {e}").pack(pady=10)

    def apply_filters(self):
        """Filter self.all_listings by query/category/price and render."""
        q_text = (self.query_var.get() or "").strip().lower()
        category = (self.category_var.get() or "All").strip()
        mn = self._num(self.min_price_var.get())
        mx = self._num(self.max_price_var.get())

        filtered = []
        for listing in self.all_listings:
            title = listing.get("title", "")
            desc = listing.get("description", "")
            cat = (listing.get("category") or "").strip()
            price = self._num(listing.get("price"))

            if q_text and q_text not in f"{title} {desc}".lower():
                continue

            # category match 
            if category != "All" and cat != category:
                continue

            # price range
            if mn is not None and (price is None or price < mn):
                continue
            if mx is not None and (price is None or price > mx):
                continue

            filtered.append(listing)

        # Render results
        for w in self.scrollable_frame.winfo_children():
            w.destroy()

        if not filtered:
            ctk.CTkLabel(self.scrollable_frame, text="No listings match your filters.", text_color="gray").pack(pady=10)
            return

        for listing in filtered:
            self.render_listing(listing)


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

        # Bookmark Button
        ctk.CTkButton(container, text="Bookmark", command=lambda id=listing["id"]: self.add_bookmark(id)).pack(anchor="w", padx=10, pady=(0, 5))

        # Image display
        if image_url:
            try:
                image = self.load_image_from_url(image_url)
                img_label = ctk.CTkLabel(container, image=image, text="")
                img_label.image = image 
                img_label.pack(padx=10, pady=10)
            except Exception as e:
                ctk.CTkLabel(container, text=f"Failed to load image: {e}").pack(padx=10, pady=(0, 10))

    def load_image_from_url(self, url):
        response = requests.get(url)
        img_data = response.content
        pil_image = Image.open(BytesIO(img_data))
        pil_image = pil_image.resize((300, 200))
        return ImageTk.PhotoImage(pil_image)

    def add_bookmark(self, listing_id):
        user_id = get_user_id()
        if not user_id:
            messagebox.showerror("Error", "You must be logged in to bookmark listings.")
            return

        try:
            response = supabase.table("Bookmarks").insert({
                "user_id": user_id,
                "listing_id": listing_id
            }).execute()

            if response.data:
                messagebox.showinfo("Bookmarked", "Listing added to your bookmarks!")
            else:
                messagebox.showerror("Error", "Failed to add bookmark. It might already be bookmarked.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def _num(self, v):
        try:
            if v is None:
                return None
            s = str(v).strip()
            if s == "":
                return None
            return float(s)
        except Exception:
            return None

    def clear_filters(self):
        """Reset filters to defaults and show all listings again."""
        self.query_var.set("")
        self.min_price_var.set("")
        self.max_price_var.set("")
        self.category_var.set("All")
        self.apply_filters()
