import tkinter as tk
from tkinter import messagebox
from datetime import datetime  # <-- needed for date/time

from depot import DepotMenu
from supply import SupplyMenu
from IT import ITMenu
from maintenance import MaintenanceMenu
from system_admin import SystemAdminMenu



class MainApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("GB Manufacturing Login")
        self.window.state("zoomed")
        self.window.configure(bg="#1e1e1e")

        # ---------------- DEFAULT USERS (RESTORED) ----------------
        self.USERS = {
            "depot": {
                "password": "123depot",
                "employee_id": "EMPD1",
                "department": "Depot"
            },
            "main": {
                "password": "123main",
                "employee_id": "EMPM1",
                "department": "Maintenance"
            },
            "sup": {
                "password": "123sup",
                "employee_id": "EMPS1",
                "department": "Supply"
            },
            "it": {
                "password": "123it",
                "employee_id": "EMPI1",
                "department": "IT"
            },
            "sysadmin": {
                "password": "123sys",
                "employee_id": "EMPSA1",
                "department": "SystemAdmin"
            }
        }

        self.build_login_screen()
        self.window.mainloop()

    # ---------------- LOGIN SCREEN ----------------
    def build_login_screen(self):
        frame = tk.Frame(self.window, bg="#1e1e1e")
        frame.pack(expand=True)

        # ----- CIRCLE LOGO -----
        canvas = tk.Canvas(frame, width=200, height=200,
                           bg="#1e1e1e", highlightthickness=0)
        canvas.pack(pady=10)

        # Circle
        canvas.create_oval(10, 10, 190, 190, outline="white", width=4)

        # Text inside circle
        canvas.create_text(100, 70, text="GB",
                           fill="white", font=("Arial", 34, "bold"))
        canvas.create_text(100, 115, text="MANUFACTURING",
                           fill="white", font=("Arial", 12, "bold"))

        # ----- DATE & TIME -----
        now = datetime.now().strftime("%A, %B %d, %Y | %I:%M %p")
        tk.Label(frame, text=now, font=("Arial", 12),
                 fg="white", bg="#1e1e1e").pack(pady=5)

        # ----- USERNAME -----
        tk.Label(frame, text="Username:",
                 fg="white", bg="#1e1e1e", font=("Arial", 14)).pack(pady=(20, 5))
        self.username_entry = tk.Entry(frame, font=("Arial", 14), width=25)
        self.username_entry.pack(pady=5)

        # ----- PASSWORD -----
        tk.Label(frame, text="Password:",
                 fg="white", bg="#1e1e1e", font=("Arial", 14)).pack(pady=(20, 5))
        self.password_entry = tk.Entry(frame, font=("Arial", 14),
                                       show="*", width=25)
        self.password_entry.pack(pady=5)

        # ----- LOGIN BUTTON -----
        tk.Button(
            frame,
            text="LOGIN",
            font=("Arial", 14, "bold"),
            width=15,
            bg="#3a7bd5",
            fg="white",
            command=self.validate_login
        ).pack(pady=30)

    # ---------------- LOGIN VALIDATION ----------------
    def validate_login(self):
        username = self.username_entry.get().lower()
        password = self.password_entry.get()

        if username not in self.USERS:
            messagebox.showerror("Error", "Invalid username")
            return

        user = self.USERS[username]

        if password != user["password"]:
            messagebox.showerror("Error", "Incorrect password")
            return

        department = user["department"]
        employee_id = user["employee_id"]

        self.window.withdraw()

        if department == "Depot":
            DepotMenu(employee_id).open_depot_menu()
        elif department == "Maintenance":
            MaintenanceMenu(employee_id).open_maintenance_menu()
        elif department == "Supply":
            SupplyMenu(employee_id).open_supply_menu()
        elif department == "IT":
            ITMenu(employee_id).open_it_menu()
        elif department == "SystemAdmin":
            SystemAdminMenu(employee_id).open_system_admin_menu()
        else:
            messagebox.showerror("Error", "Unknown department")


if __name__ == "__main__":
    MainApp()
