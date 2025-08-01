import customtkinter

# === Main App Window ===
app = customtkinter.CTk()
app.geometry("1440x960")
app.title("Vaquero Marketplace")
app.configure(fg_color="white")

# === Pages as Frames ===
login_page = customtkinter.CTkFrame(app, fg_color="white")
signup_page = customtkinter.CTkFrame(app, fg_color="white")
home_page = customtkinter.CTkFrame(app, fg_color="white")

for page in (login_page, signup_page, home_page):
    page.place(relwidth=1, relheight=1)

# === Page Switcher ===
def show_page(page):
    page.tkraise()

# === Login Page ===
def build_login_page():
    top = customtkinter.CTkFrame(login_page, fg_color="white")
    top.pack(pady=25, fill="x")

    customtkinter.CTkLabel(top, text="Welcome to Vaquero Marketplace",
                           text_color="#ec6f05", font=("Georgia", 30, "bold")).pack(side="left", padx=20)

    sidebar = customtkinter.CTkFrame(login_page, width=160, height=1000,
                                     fg_color="#ec6f05", corner_radius=0)
    sidebar.place(relx=1.0, rely=0, anchor="ne")

    center = customtkinter.CTkFrame(login_page, width=800, height=600,
                                    corner_radius=10, fg_color="#D9D9D9")
    center.pack(pady=30)

    customtkinter.CTkLabel(center, text="Log In",
                           font=("Georgia", 18), text_color="black").pack(pady=(20, 10))

    customtkinter.CTkEntry(center, placeholder_text="Username or Email", width=250).pack(pady=10)
    customtkinter.CTkEntry(center, placeholder_text="Password", width=250, show="*").pack(pady=10)

    customtkinter.CTkButton(center, text="Log In", width=250,
                            fg_color="#ec6f05", hover_color="#d95e00",
                            command=lambda: show_page(home_page)).pack(pady=20)

    customtkinter.CTkButton(center, text="Create new account", width=200,
                            fg_color="white", text_color="black",
                            border_color="black", border_width=1,
                            command=lambda: show_page(signup_page)).pack(pady=5)

# === Sign Up Page ===
def build_signup_page():
    top = customtkinter.CTkFrame(signup_page, fg_color="white")
    top.pack(pady=25, fill="x")

    customtkinter.CTkLabel(top, text="Welcome to Vaquero Marketplace",
                           text_color="#ec6f05", font=("Georgia", 30, "bold")).pack(side="left", padx=20)

    sidebar = customtkinter.CTkFrame(signup_page, width=160, height=1000,
                                     fg_color="#ec6f05", corner_radius=0)
    sidebar.place(relx=1.0, rely=0, anchor="ne")

    center = customtkinter.CTkFrame(signup_page, width=800, height=600,
                                    corner_radius=10, fg_color="#D9D9D9")
    center.pack(pady=30)

    customtkinter.CTkLabel(center, text="Sign Up",
                           font=("Georgia", 18), text_color="black").pack(pady=(20, 10))

    customtkinter.CTkEntry(center, placeholder_text="Name", width=250).pack(pady=10)
    customtkinter.CTkEntry(center, placeholder_text="Email", width=250).pack(pady=10)
    customtkinter.CTkEntry(center, placeholder_text="Password", width=250, show="*").pack(pady=10)

    customtkinter.CTkButton(center, text="Sign Up", width=250,
                            fg_color="#ec6f05", hover_color="#d95e00",
                            command=lambda: show_page(home_page)).pack(pady=20)

    customtkinter.CTkButton(center, text="Already have an account?", width=200,
                            fg_color="white", text_color="black",
                            border_color="black", border_width=1,
                            command=lambda: show_page(login_page)).pack(pady=5)

# === Home Page ===
def build_home_page():
    # Top Bar
    top_frame = customtkinter.CTkFrame(home_page, fg_color="orange", height=60)
    top_frame.pack(fill="x", side="top")

    customtkinter.CTkLabel(top_frame, text="🟧 Vaquero Marketplace",
                           font=("Georgia", 20, "bold")).pack(side="left", padx=10)

    customtkinter.CTkEntry(top_frame, placeholder_text="Search", width=300).pack(side="left", padx=20)

    user_circle = customtkinter.CTkLabel(top_frame, text="C R", font=("Arial", 16, "bold"),
                                         text_color="black", width=40, height=40,
                                         corner_radius=20, fg_color="white")
    user_circle.pack(side="right", padx=10)

    customtkinter.CTkButton(top_frame, text="Log Off", width=60, fg_color="white",
                            text_color="black", command=lambda: show_page(login_page)).pack(side="right", padx=10)

    # Navigation
    nav_frame = customtkinter.CTkFrame(home_page, fg_color="white", height=60)
    nav_frame.pack(fill="x", pady=10)

    customtkinter.CTkButton(nav_frame, text="🏠 Home / Feed", width=120, fg_color="orange").pack(side="left", padx=10)
    customtkinter.CTkButton(nav_frame, text="🖤 Favorites", width=120, fg_color="lightgray", text_color="black").pack(side="left", padx=10)
    customtkinter.CTkButton(nav_frame, text="➕ Add Listing", width=120, fg_color="lightgray", text_color="black").pack(side="left", padx=10)
    customtkinter.CTkButton(nav_frame, text="👤 My Listings", width=120, fg_color="lightgray", text_color="black").pack(side="left", padx=10)

    # Feed Content
    feed_frame = customtkinter.CTkFrame(home_page, fg_color="white")
    feed_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def create_listing_card(parent):
        card = customtkinter.CTkFrame(parent, width=200, height=240, fg_color="white",
                                      corner_radius=10, border_color="gray", border_width=1)
        img_label = customtkinter.CTkLabel(card, text="IMG", width=180, height=120, text_color="gray",
                                           fg_color="#f5f5f5", corner_radius=5)
        img_label.pack(pady=10)

        title_label = customtkinter.CTkLabel(card, text="Title", font=("Arial", 12))
        title_label.pack(pady=5)

        view_btn = customtkinter.CTkButton(card, text="View details", width=100, height=30,
                                           fg_color="lightgray", text_color="black")
        view_btn.pack(pady=5)

        return card

    for i in range(2):
        for j in range(3):
            card = create_listing_card(feed_frame)
            card.grid(row=i, column=j, padx=20, pady=20)

# === Build All Pages ===
build_login_page()
build_signup_page()
build_home_page()

# === Start on Login Page ===
show_page(login_page)

# === Run App ===
app.mainloop()
