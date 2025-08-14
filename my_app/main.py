# main.py
import customtkinter as ctk
from .auth.login_window import LoginWindow
from .views.main_dashboard import MainDashboard  

ctk.set_appearance_mode("light")  # or "dark"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Vaquero Marketplace")
        self.geometry("800x600")  # match your dashboard size

        self.frames = {}

        # ✅ Initialize login page
        login = LoginWindow(self, self)
        login.pack(fill="both", expand=True)
        self.frames["LoginWindow"] = login

        # ✅ Initialize dashboard page
        dashboard = MainDashboard(self, self)
        dashboard.pack_forget()  # don't show yet
        self.frames["Dashboard"] = dashboard

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()

        frame = self.frames.get(frame_name)
        if frame:
            frame.pack(fill="both", expand=True)
        else:
            print(f"No frame found: {frame_name}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
