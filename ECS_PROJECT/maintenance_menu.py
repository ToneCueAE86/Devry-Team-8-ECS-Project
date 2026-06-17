import tkinter as tk
from tkinter import messagebox

BG = "#e6e6e6"
BTN_BG = "#c0c0c0"
FG = "black"

# Reuse header from main.py
def build_header(parent):
    from main import build_header as main_header
    main_header(parent)


class MaintenanceMenu:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=BG)
        self.root.state("zoomed")

        # Center frame
        center = tk.Frame(root, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        build_header(center)

        # Title
        tk.Label(center,
                 text="MAINTENANCE DEPARTMENT",
                 font=("Arial", 28, "bold"),
                 bg=BG, fg=FG).pack(pady=20)

        # Maintenance Menu Buttons
        menu_items = [
            "Submit Work Order",
            "View Assigned Tasks",
            "Equipment Maintenance Logs",
            "Request Tools",
            "Safety Checklist",
            "Maintenance Reports"
        ]

        for item in menu_items:
            tk.Button(center,
                      text=item,
                      font=("Arial", 18),
                      width=35,
                      height=2,
                      bg=BTN_BG,
                      fg=FG,
                      command=self.under_construction).pack(pady=10)

        # Logout Button
        tk.Button(center,
                  text="Logout",
                  font=("Arial", 18),
                  width=20,
                  height=1,
                  bg=BTN_BG,
                  fg=FG,
                  command=self.logout).pack(pady=25)

    # Under Construction Message
    def under_construction(self):
        messagebox.showinfo(
            "Coming Soon",
            "This feature is under construction and not yet available."
        )

    # Logout → Back to Login Screen
    def logout(self):
        from main import LoginWindow
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginWindow(self.root)
