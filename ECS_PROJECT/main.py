import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ===== IMPORT DEPARTMENT MENUS =====
from depot import DepotMenu
from it_menu import ITMenu
from maintenance_menu import MaintenanceMenu
from supply_menu import SupplyMenu
from sysadmin_menu import SysAdminMenu

# ===== COLORS =====
BG = "#e6e6e6"
BTN_BG = "#c0c0c0"
FG = "black"

# ===== DEFAULT USER ACCOUNTS =====
USERS = {
    "depot_user": {
        "password": "depot123",
        "department": "depot"
    },
    "it_user": {
        "password": "it123",
        "department": "it"
    },
    "maint_user": {
        "password": "maint123",
        "department": "maintenance"
    },
    "supply_user": {
        "password": "supply123",
        "department": "supply"
    },
    "admin_user": {
        "password": "admin123",
        "department": "sysadmin"
    }
}


# ===== HEADER BUILDER =====
def build_header(parent):
    header = tk.Frame(parent, bg=BG)
    header.pack(pady=10)

    canvas = tk.Canvas(header, width=300, height=300,
                       bg=BG, highlightthickness=0)
    canvas.pack()

    canvas.create_oval(10, 10, 290, 290, outline="black", width=6)
    canvas.create_text(150, 120, text="GB",
                       fill="black", font=("Arial", 64, "bold"))
    canvas.create_text(150, 185, text="MANUFACTURING",
                       fill="black", font=("Arial", 20, "bold"))

    now = datetime.now().strftime("%A, %B %d, %Y | %I:%M %p")
    tk.Label(header, text=now, font=("Arial", 14),
             fg=FG, bg=BG).pack(pady=6)


# ===== LOGIN WINDOW =====
class LoginWindow:
    def __init__(self, root):
        self.root = root

        # Fullscreen
        self.root.state("zoomed")
        self.root.configure(bg=BG)

        # Center container
        center = tk.Frame(root, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        build_header(center)

        tk.Label(center, text="LOGIN",
                 font=("Arial", 26, "bold"),
                 bg=BG, fg=FG).pack(pady=20)

        # Username
        tk.Label(center, text="Username:",
                 font=("Arial", 16), bg=BG, fg=FG).pack()
        self.username_entry = tk.Entry(center, font=("Arial", 16), width=30)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(center, text="Password:",
                 font=("Arial", 16), bg=BG, fg=FG).pack()
        self.password_entry = tk.Entry(center, font=("Arial", 16),
                                       width=30, show="*")
        self.password_entry.pack(pady=5)

        # Department
        tk.Label(center, text="Department:",
                 font=("Arial", 16), bg=BG, fg=FG).pack()
        self.dept_entry = tk.Entry(center, font=("Arial", 16), width=30)
        self.dept_entry.pack(pady=5)

        # Login button
        tk.Button(center,
                  text="Login",
                  font=("Arial", 16),
                  width=15,
                  bg=BTN_BG,
                  fg=FG,
                  command=self.handle_login).pack(pady=20)

    # ===== LOGIN VALIDATION =====
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        dept = self.dept_entry.get().strip().lower()

        # Validate username
        if username not in USERS:
            messagebox.showerror("Login Failed", "Invalid username.")
            return

        # Validate password
        if USERS[username]["password"] != password:
            messagebox.showerror("Login Failed", "Incorrect password.")
            return

        # Validate department
        if USERS[username]["department"] != dept:
            messagebox.showerror("Login Failed",
                                 "Department does not match user account.")
            return

        # Clear screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # ===== ROUTE TO CORRECT DEPARTMENT =====
        if dept == "depot":
            DepotMenu(self.root)

        elif dept == "it":
            ITMenu(self.root)

        elif dept == "maintenance":
            MaintenanceMenu(self.root)

        elif dept == "supply":
            SupplyMenu(self.root)

        elif dept == "sysadmin":
            SysAdminMenu(self.root)

        else:
            messagebox.showerror("Login Failed", "Unknown department.")


# ===== MAIN =====
if __name__ == "__main__":
    root = tk.Tk()
    root.title("ECS System")
    LoginWindow(root)
    root.mainloop()
