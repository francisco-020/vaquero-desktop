# main.py
import customtkinter as ctk
from .auth.login_window import LoginWindow # import login window
from .views.main_dashboard import MainDashboard  # import dashboard view

# Set global appearance for the app
ctk.set_appearance_mode("light")  
ORANGE = "#EC6F05"
ORANGE_HOVER = "#DC6600"
WHITE = "#FFFFFF"

def _patch_orange_defaults():
    _orig_btn_init = ctk.CTkButton.__init__
    def _orange_btn_init(self, *args, **kwargs):
        kwargs.setdefault("fg_color", ORANGE)
        kwargs.setdefault("hover_color", ORANGE_HOVER)
        kwargs.setdefault("text_color", WHITE)
        return _orig_btn_init(self, *args, **kwargs)
    ctk.CTkButton.__init__ = _orange_btn_init

    _orig_opt_init = ctk.CTkOptionMenu.__init__
    def _orange_opt_init(self, *args, **kwargs):
        kwargs.setdefault("fg_color", ORANGE)              
        kwargs.setdefault("button_color", ORANGE)          
        kwargs.setdefault("button_hover_color", ORANGE_HOVER)
        kwargs.setdefault("text_color", WHITE)
        return _orig_opt_init(self, *args, **kwargs)
    ctk.CTkOptionMenu.__init__ = _orange_opt_init

_patch_orange_defaults()

# Main application class, handles switching between Login and Dashboard pages
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Vaquero Marketplace")
        self.geometry("800x600")  

        # Store references to all frames/pages
        self.frames = {}

        # Initialize login page, this will be the first screen user will see
        login = LoginWindow(self, self)
        login.pack(fill="both", expand=True)
        self.frames["LoginWindow"] = login

        # Initialize dashboard page, this is hidden until after login
        dashboard = MainDashboard(self, self)
        dashboard.pack_forget()  # don't show yet
        self.frames["Dashboard"] = dashboard

    # Hides all frames and only shows the requested frame
    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()

        frame = self.frames.get(frame_name)
        if frame:
            frame.pack(fill="both", expand=True)
        else:
            print(f"No frame found: {frame_name}")

if __name__ == "__main__":
    # Starts application
    app = App()
    app.mainloop()
