import tkinter as tk
from datetime import datetime

class ITMenu:
    def __init__(self, username):
        self.username = username

    def open_it_menu(self):
        # Create the window
        self.window = tk.Toplevel()
        win = self.window

        win.title("IT Department Menu")
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
            text="IT Department",
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
        menu_button("Reset User Passwords").pack(pady=10)
        menu_button("Unlock User Accounts").pack(pady=10)
        menu_button("View System Logs").pack(pady=10)
        menu_button("Run Diagnostics").pack(pady=10)
        menu_button("Backup / Restore Database").pack(pady=10)

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
