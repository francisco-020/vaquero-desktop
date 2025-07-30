import customtkinter

# Global appearance settings (optional)
customtkinter.set_appearance_mode("System")  # "Light" or "Dark" or "System"
customtkinter.set_default_color_theme("blue")  # "blue", "green", "dark-blue", etc.

# Create the main window
app = customtkinter.CTk()
app.title("Desktop Summer App")
app.geometry("400x300")  # Optional: set size

# Input field
entry = customtkinter.CTkEntry(app, placeholder_text="First Name")
entry.pack(pady=20)

# Label that will display radio button value
labelR = customtkinter.CTkLabel(app, text="")
labelR.pack(pady=10)

# Function to update label when radio button is selected
def rbutton(value):
    labelR.configure(text=f"Selected: {value}")

# IntVar for radio buttons
var = customtkinter.IntVar()

# Radio buttons
radio1 = customtkinter.CTkRadioButton(app, text="Option 1", variable=var, value=1, command=lambda: rbutton(var.get()))
radio2 = customtkinter.CTkRadioButton(app, text="Option 2", variable=var, value=2, command=lambda: rbutton(var.get()))
radio3 = customtkinter.CTkRadioButton(app, text="Option 3", variable=var, value=3, command=lambda: rbutton(var.get()))

radio1.pack()
radio2.pack()
radio3.pack()

# Run the app
app.mainloop()
