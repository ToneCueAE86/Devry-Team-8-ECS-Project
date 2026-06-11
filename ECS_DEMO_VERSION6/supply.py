import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class SupplyMenu:
    def __init__(self, username):
        self.username = username

    def open_supply_menu(self):
        # Create the window
        self.window = tk.Toplevel()
        win = self.window

        win.title("Supply Department Menu")
        win.state("zoomed")
        win.configure(bg="#1e1e1e")

        # ---------------- HEADER ----------------
        header = tk.Frame(win, bg="#1e1e1e")
        header.pack(fill="x", pady=10)

        tk.Label(
            header,
            text="GB MANUFACTURING",
            font=("Arial", 26, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack()

        now = datetime.now().strftime("%A, %B %d, %Y | %I:%M %p")
        tk.Label(
            header,
            text=now,
            font=("Arial", 12),
            fg="white",
            bg="#1e1e1e"
        ).pack()

        tk.Label(
            header,
            text="Supply Department",
            font=("Arial", 14, "bold"),
            fg="#3a7bd5",
            bg="#1e1e1e"
        ).pack(pady=(5, 20))

        # ---------------- MAIN MENU AREA ----------------
        frame = tk.Frame(win, bg="#1e1e1e")
        frame.pack(expand=True)

        # Button style helper
        def menu_button(text, command=None):
            return tk.Button(
                frame,
                text=text,
                font=("Arial", 16),
                width=30,
                height=2,
                bg="#3a3a3a",
                fg="white",
                bd=2,
                relief="raised",
                command=command
            )

        # ---------------- BUTTONS (MATCHING YOUR PHOTO) ----------------
        menu_button("Add New Equipment").pack(pady=10)
        menu_button("Replace Equipment").pack(pady=10)
        menu_button("Decommission Equipment").pack(pady=10)
        menu_button("Update Inventory Quantities").pack(pady=10)
        menu_button("View Equipment List").pack(pady=10)

        # Logout button
        tk.Button(
            frame,
            text="Logout",
            font=("Arial", 16),
            width=20,
            bg="#5a5a5a",
            fg="white",
            command=win.destroy
        ).pack(pady=40)
