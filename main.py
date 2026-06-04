import tkinter as tk
from datetime import datetime, timedelta

LOG_FILE = "system_logs.txt"
INACTIVITY_DAYS = 30


# -------------------------
# LOGGER
# -------------------------
class Logger:
    def __init__(self):
        self.entries = []

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp} — {message}"
        self.entries.append(line)
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass

    def get_all(self):
        return "\n".join(self.entries)


# -------------------------
# USER STORE
# -------------------------
class UserStore:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.users = {
            "sysadmin": {
                "password": "admin123",
                "role": "System Administrator",
                "bootstrap": True,
                "locked": False,
                "disabled": False,
                "created_at": datetime.now(),
                "last_activity": datetime.now()
            }
        }
        self.real_sysadmin_created = False

    def _check_and_maybe_disable_for_inactivity(self, user: dict, username: str):
        if user.get("disabled"):
            return
        last = user.get("last_activity") or user.get("created_at") or datetime.now()
        if datetime.now() - last > timedelta(days=INACTIVITY_DAYS):
            user["disabled"] = True
            self.logger.log(f"Account disabled due to inactivity for user: {username}")

    def record_activity_for_username(self, username: str):
        user = self.users.get(username)
        if not user:
            return
        # First check if they should be disabled
        self._check_and_maybe_disable_for_inactivity(user, username)
        if user.get("disabled"):
            return
        # Correct username = activity refresh
        user["last_activity"] = datetime.now()

    def validate_user(self, username: str, password: str):
        user = self.users.get(username)
        if not user:
            self.logger.log(f"Login failed for unknown user: {username}")
            return None, "invalid"

        if user.get("disabled"):
            self.logger.log(f"Login attempt for disabled user: {username}")
            return None, "disabled"

        if user.get("locked"):
            self.logger.log(f"Login attempt for locked user: {username}")
            return None, "locked"

        if user["password"] != password:
            self.logger.log(f"Login failed for user: {username}")
            return None, "invalid"

        # Successful login
        user["last_activity"] = datetime.now()
        self.logger.log(f"Login success for user: {username}")
        return user, "ok"

    def add_user(self, username: str, password: str, department_as_role: str, extra=None):
        if username in self.users:
            return False
        data = {
            "password": password,
            "role": department_as_role,   # Department = Role
            "bootstrap": False,
            "locked": False,
            "disabled": False,
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        if extra:
            data.update(extra)
        self.users[username] = data
        self.logger.log(f"Account created for user: {username} (role: {department_as_role})")
        return True

    def mark_real_sysadmin_created(self):
        self.real_sysadmin_created = True
        if "sysadmin" in self.users:
            self.users["sysadmin"]["locked"] = True
            self.logger.log("Bootstrap sysadmin account locked permanently")

    def has_real_sysadmin(self):
        return self.real_sysadmin_created

    def reset_password(self, operator: str, target_username: str, new_password: str):
        user = self.users.get(target_username)
        if not user:
            return False
        user["password"] = new_password
        self.logger.log(f"Password reset for user: {target_username} by {operator}")
        return True

    def unlock_account(self, operator: str, target_username: str):
        user = self.users.get(target_username)
        if not user:
            return False
        user["disabled"] = False
        user["locked"] = False
        user["last_activity"] = datetime.now()
        self.logger.log(f"Account unlocked for user: {target_username} by {operator}")
        return True


# -------------------------
# BASE WINDOW WITH HEADER
# -------------------------
class BaseWindow(tk.Tk):
    def __init__(self, title_text):
        super().__init__()
        self.title(title_text)
        self.state("zoomed")
        self.datetime_label = None

    def build_header(self, parent):
        header = tk.Frame(parent)
        header.pack(pady=20)

        canvas = tk.Canvas(header, width=220, height=220, highlightthickness=0)
        canvas.pack()
        canvas.create_oval(10, 10, 210, 210, width=4)
        canvas.create_text(110, 90, text="GB", font=("Arial", 40, "bold"))
        canvas.create_text(110, 140, text="Manufacturing", font=("Arial", 16))

        tk.Label(parent, text="Equipment Management System (EMS)", font=("Arial", 20)).pack(pady=5)

        self.datetime_label = tk.Label(parent, text="", font=("Arial", 14))
        self.datetime_label.pack(pady=5)
        self.update_datetime()

    def update_datetime(self):
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M %p")
        if self.datetime_label:
            self.datetime_label.config(text=f"{date_str} | {time_str}")
        self.after(1000, self.update_datetime)


# -------------------------
# LOGIN SCREEN
# -------------------------
class LoginScreen(BaseWindow):
    def __init__(self, user_store: UserStore, logger: Logger):
        super().__init__("GB Manufacturing - Equipment Management System")
        self.user_store = user_store
        self.logger = logger
        self.username_entry = None
        self.password_entry = None
        self.status_label = None
        self.build_ui()

    def build_ui(self):
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)

        self.build_header(frame)

        user_frame = tk.Frame(frame)
        user_frame.pack(pady=15)
        tk.Label(user_frame, text="Username:", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(user_frame, width=25, font=("Arial", 16))
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        pass_frame = tk.Frame(frame)
        pass_frame.pack(pady=15)
        tk.Label(pass_frame, text="Password:", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(pass_frame, width=25, font=("Arial", 16), show="*")
        self.password_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(frame, text="Login", width=25, font=("Arial", 16), command=self.handle_login).pack(pady=30)

        self.status_label = tk.Label(frame, text="", font=("Arial", 12), fg="red")
        self.status_label.pack(pady=5)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Correct username counts as activity (if not yet disabled)
        if username in self.user_store.users:
            self.user_store.record_activity_for_username(username)

        user, status = self.user_store.validate_user(username, password)

        if status == "disabled":
            self.status_label.config(text="Your account is disabled due to inactivity. Please contact IT.")
            return
        if status == "locked":
            self.status_label.config(text="Your account is locked. Please contact IT.")
            return
        if status == "invalid":
            self.status_label.config(text="Invalid username or password.")
            return

        role = user["role"]
        is_bootstrap = user.get("bootstrap", False)

        self.destroy()

        if is_bootstrap and not self.user_store.has_real_sysadmin():
            SystemAdminSetup(self.user_store, self.logger)
        else:
            if role == "System Administrator":
                SystemAdminMenu(self.user_store, self.logger, username, role)
            else:
                RoleMenu(self.user_store, self.logger, username, role)


# -------------------------
# SYSTEM ADMIN SETUP (FIRST RUN)
# -------------------------
class SystemAdminSetup(BaseWindow):
    DEPARTMENTS = [
        "System Administrator",
        "IT Department",
        "Supply Department",
        "Equipment Depot",
        "Maintenance",
        "Special Projects",
        "Supervisor / Manager",
        "Other"
    ]

    def __init__(self, user_store: UserStore, logger: Logger):
        super().__init__("GB Manufacturing - EMS - System Administrator Setup")
        self.user_store = user_store
        self.logger = logger
        self.entries = {}
        self.dept_var = tk.StringVar(value=self.DEPARTMENTS[0])
        self.dept_other_entry = None
        self.status_label = None
        self.build_ui()
        self.mainloop()

    def build_ui(self):
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)

        self.build_header(frame)

        tk.Label(frame, text="Create System Administrator Account", font=("Arial", 18, "bold")).pack(pady=10)

        form = tk.Frame(frame)
        form.pack(pady=10)

        def add_field(label, key, row):
            tk.Label(form, text=label, font=("Arial", 12)).grid(row=row, column=0, padx=10, pady=5, sticky="e")
            e = tk.Entry(form, width=30, font=("Arial", 12))
            e.grid(row=row, column=1, padx=10, pady=5)
            self.entries[key] = e

        add_field("First Name:", "first_name", 0)
        add_field("Last Name:", "last_name", 1)
        add_field("Employee ID:", "employee_id", 2)

        tk.Label(form, text="Department:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        dept_menu = tk.OptionMenu(form, self.dept_var, *self.DEPARTMENTS, command=self.on_dept_change)
        dept_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form, text="Position / Title:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entries["position"] = tk.Entry(form, width=30, font=("Arial", 12))
        self.entries["position"].grid(row=4, column=1, padx=10, pady=5)

        add_field("Phone Number:", "phone", 5)
        add_field("Email:", "email", 6)
        add_field("Username:", "username", 7)
        add_field("Password:", "password", 8)
        self.entries["password"].config(show="*")

        tk.Button(
            frame,
            text="Create System Administrator Account",
            font=("Arial", 14),
            width=35,
            command=self.create_sysadmin
        ).pack(pady=20)

        self.status_label = tk.Label(frame, text="", font=("Arial", 12), fg="red")
        self.status_label.pack(pady=5)

    def on_dept_change(self, value):
        form = self.children["!frame"].children["!frame"]
        if value == "Other":
            if not self.dept_other_entry:
                self.dept_other_entry = tk.Entry(form, width=30, font=("Arial", 12))
                self.dept_other_entry.grid(row=3, column=2, padx=10, pady=5)
        else:
            if self.dept_other_entry:
                self.dept_other_entry.destroy()
                self.dept_other_entry = None

    def create_sysadmin(self):
        data = {k: e.get().strip() for k, e in self.entries.items()}
        if any(not v for v in data.values()):
            self.status_label.config(text="All fields are required.")
            return

        dept = self.dept_var.get()
        if dept == "Other":
            if not self.dept_other_entry or not self.dept_other_entry.get().strip():
                self.status_label.config(text="Please specify Department (Other).")
                return
            dept = self.dept_other_entry.get().strip()

        username = data["username"]
        password = data["password"]

        extra = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "employee_id": data["employee_id"],
            "department": dept,
            "position": data["position"],
            "phone": data["phone"],
            "email": data["email"]
        }

        if not self.user_store.add_user(username, password, dept, extra=extra):
            self.status_label.config(text="Username already exists. Choose another.")
            return

        self.user_store.mark_real_sysadmin_created()
        self.destroy()
        SystemAdminMenu(self.user_store, self.logger, username, "System Administrator")


# -------------------------
# CREATE USER ACCOUNT WINDOW
# -------------------------
class CreateUserWindow(tk.Toplevel):
    DEPARTMENTS = [
        "System Administrator",
        "IT Department",
        "Supply Department",
        "Equipment Depot",
        "Maintenance",
        "Special Projects",
        "Supervisor / Manager",
        "Other"
    ]

    def __init__(self, parent, user_store: UserStore, logger: Logger, operator_username: str):
        super().__init__(parent)
        self.title("System Administrator - Create User Account")
        self.geometry("700x520")
        self.user_store = user_store
        self.logger = logger
        self.operator = operator_username

        self.entries = {}
        self.dept_var = tk.StringVar(value=self.DEPARTMENTS[1])
        self.dept_other_entry = None
        self.status_label = None

        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Create New User Account", font=("Arial", 16, "bold")).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=10)

        def add_field(label, key, row):
            tk.Label(form, text=label, font=("Arial", 12)).grid(row=row, column=0, padx=10, pady=5, sticky="e")
            e = tk.Entry(form, width=30, font=("Arial", 12))
            e.grid(row=row, column=1, padx=10, pady=5)
            self.entries[key] = e

        add_field("First Name:", "first_name", 0)
        add_field("Last Name:", "last_name", 1)
        add_field("Employee ID:", "employee_id", 2)

        tk.Label(form, text="Department:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        dept_menu = tk.OptionMenu(form, self.dept_var, *self.DEPARTMENTS, command=self.on_dept_change)
        dept_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form, text="Position / Title:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entries["position"] = tk.Entry(form, width=30, font=("Arial", 12))
        self.entries["position"].grid(row=4, column=1, padx=10, pady=5)

        add_field("Phone Number:", "phone", 5)
        add_field("Email:", "email", 6)
        add_field("Username:", "username", 7)
        add_field("Password:", "password", 8)
        self.entries["password"].config(show="*")

        self.status_label = tk.Label(self, text="", font=("Arial", 11))
        self.status_label.pack(pady=5)

        bottom = tk.Frame(self)
        bottom.pack(fill="x", pady=15, padx=20)

        # EXIT bottom-left, same default style
        tk.Button(bottom, text="Exit", font=("Arial", 12), width=12, command=self.close_window).pack(side="left")

        # Create Account bottom-right
        tk.Button(bottom, text="Create Account", font=("Arial", 12), width=15, command=self.create_user).pack(
            side="right"
        )

    def on_dept_change(self, value):
        form = self.children["!frame"]
        if value == "Other":
            if not self.dept_other_entry:
                self.dept_other_entry = tk.Entry(form, width=30, font=("Arial", 12))
                self.dept_other_entry.grid(row=3, column=2, padx=10, pady=5)
        else:
            if self.dept_other_entry:
                self.dept_other_entry.destroy()
                self.dept_other_entry = None

    def close_window(self):
        self.destroy()  # Return to System Admin Menu (parent still open)

    def create_user(self):
        data = {k: e.get().strip() for k, e in self.entries.items()}
        if any(not v for v in data.values()):
            self.status_label.config(text="All fields are required.", fg="red")
            return

        dept = self.dept_var.get()
        if dept == "Other":
            if not self.dept_other_entry or not self.dept_other_entry.get().strip():
                self.status_label.config(text="Please specify Department (Other).", fg="red")
                return
            dept = self.dept_other_entry.get().strip()

        username = data["username"]
        password = data["password"]

        extra = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "employee_id": data["employee_id"],
            "department": dept,
            "position": data["position"],
            "phone": data["phone"],
            "email": data["email"]
        }

        if not self.user_store.add_user(username, password, dept, extra=extra):
            self.status_label.config(text="Username already exists. Choose another.", fg="red")
            return

        self.logger.log(f"User account created by {self.operator} for {username} (role: {dept})")
        self.status_label.config(text=f"User '{username}' created successfully.", fg="green")
        for e in self.entries.values():
            e.delete(0, tk.END)


# -------------------------
# SYSTEM ADMIN MENU
# -------------------------
class SystemAdminMenu(BaseWindow):
    def __init__(self, user_store: UserStore, logger: Logger, username: str, role: str):
        super().__init__("GB Manufacturing - EMS - System Administrator Menu")
        self.user_store = user_store
        self.logger = logger
        self.username = username
        self.role = role
        self.build_ui()
        self.mainloop()

    def build_ui(self):
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)

        self.build_header(frame)

        tk.Label(frame, text=f"Logged in as: {self.username} ({self.role})", font=("Arial", 14)).pack(pady=5)
        tk.Label(frame, text="System Administrator Menu", font=("Arial", 18, "bold")).pack(pady=10)

        center = tk.Frame(frame)
        center.pack(pady=20)

        buttons = [
            ("Create User Account", self.open_create_user),
            ("Manage User Accounts", self.placeholder),
            ("Add Equipment (Supply Support)", self.placeholder),
            ("Manage Equipment Inventory", self.placeholder),
            ("View All Logs", self.view_logs),
            ("System Settings", self.placeholder),
            ("Logout", self.logout)
        ]

        for text, cmd in buttons:
            tk.Button(center, text=text, width=40, height=2, font=("Arial", 14), command=cmd).pack(pady=5)

    def open_create_user(self):
        CreateUserWindow(self, self.user_store, self.logger, self.username)

    def view_logs(self):
        win = tk.Toplevel(self)
        win.title("System Logs")
        win.geometry("800x500")
        tk.Label(win, text="System Logs", font=("Arial", 14, "bold")).pack(pady=5)
        txt = tk.Text(win, wrap="word", font=("Consolas", 10))
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("1.0", self.logger.get_all())
        txt.config(state="disabled")

    def placeholder(self):
        win = tk.Toplevel(self)
        win.title("Not Implemented Yet")
        win.geometry("400x200")
        tk.Label(win, text="This function will be implemented later.", font=("Arial", 12)).pack(pady=40)

    def logout(self):
        self.logger.log(f"Logout by user: {self.username}")
        self.destroy()
        LoginScreen(self.user_store, self.logger).mainloop()


# -------------------------
# IT PASSWORD RESET / UNLOCK WINDOWS
# -------------------------
class ResetPasswordWindow(tk.Toplevel):
    def __init__(self, parent, user_store: UserStore, logger: Logger, operator: str):
        super().__init__(parent)
        self.title("IT Department - Reset User Password")
        self.geometry("500x250")
        self.user_store = user_store
        self.logger = logger
        self.operator = operator

        self.user_entry = None
        self.pass_entry = None
        self.status_label = None
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Reset User Password", font=("Arial", 14, "bold")).pack(pady=10)
        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Username:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.user_entry = tk.Entry(form, width=25, font=("Arial", 12))
        self.user_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="New Password:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.pass_entry = tk.Entry(form, width=25, font=("Arial", 12), show="*")
        self.pass_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self, text="Reset Password", font=("Arial", 12), command=self.reset).pack(pady=15)
        self.status_label = tk.Label(self, text="", font=("Arial", 11))
        self.status_label.pack(pady=5)

    def reset(self):
        username = self.user_entry.get().strip()
        new_pass = self.pass_entry.get().strip()
        if not username or not new_pass:
            self.status_label.config(text="Username and new password required.", fg="red")
            return
        if not self.user_store.reset_password(self.operator, username, new_pass):
            self.status_label.config(text="User not found.", fg="red")
            return
        self.status_label.config(text=f"Password reset for '{username}'.", fg="green")


class UnlockAccountWindow(tk.Toplevel):
    def __init__(self, parent, user_store: UserStore, logger: Logger, operator: str):
        super().__init__(parent)
        self.title("IT Department - Unlock User Account")
        self.geometry("500x220")
        self.user_store = user_store
        self.logger = logger
        self.operator = operator

        self.user_entry = None
        self.status_label = None
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Unlock User Account", font=("Arial", 14, "bold")).pack(pady=10)
        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Username:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.user_entry = tk.Entry(form, width=25, font=("Arial", 12))
        self.user_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(self, text="Unlock Account", font=("Arial", 12), command=self.unlock).pack(pady=15)
        self.status_label = tk.Label(self, text="", font=("Arial", 11))
        self.status_label.pack(pady=5)

    def unlock(self):
        username = self.user_entry.get().strip()
        if not username:
            self.status_label.config(text="Username required.", fg="red")
            return
        if not self.user_store.unlock_account(self.operator, username):
            self.status_label.config(text="User not found.", fg="red")
            return
        self.status_label.config(text=f"Account unlocked for '{username}'.", fg="green")


# -------------------------
# ROLE MENUS (DEPARTMENT = ROLE)
# -------------------------
ROLE_MENU_OPTIONS = {
    "IT Department": [
        "Reset User Passwords",
        "Unlock User Accounts",
        "View System Logs",
        "Run Diagnostics",
        "Backup / Restore Database",
        "Logout"
    ],
    "Supply Department": [
        "Add New Equipment",
        "Replace Equipment",
        "Retire Equipment",
        "Update Inventory Quantities",
        "View Equipment List",
        "Logout"
    ],
    "Equipment Depot": [
        "Process Equipment Checkout",
        "Process Equipment Return",
        "Update Equipment Availability",
        "Mark Equipment Lost / Damaged",
        "View All Checked-Out Equipment",
        "View Overdue Equipment",
        "Logout"
    ],
    "Maintenance": [
        "Check Out Equipment",
        "Return Equipment",
        "Update Equipment Condition",
        "View My Equipment History",
        "Logout"
    ],
    "Special Projects": [
        "Check Out Equipment",
        "Return Equipment",
        "Request Restricted Equipment",
        "Update Equipment Condition",
        "View My Equipment History",
        "Logout"
    ],
    "Supervisor / Manager": [
        "Approve Restricted Equipment Requests",
        "Check Out Equipment (for team)",
        "Return Equipment (for team)",
        "View All Checked-Out Equipment",
        "View Employee Equipment History",
        "Generate Reports",
        "Logout"
    ],
    "System Administrator": [
        # Normally handled by SystemAdminMenu, but kept for safety
        "Logout"
    ]
}


class RoleMenu(BaseWindow):
    def __init__(self, user_store: UserStore, logger: Logger, username: str, role: str):
        super().__init__(f"GB Manufacturing - EMS - {role} Menu")
        self.user_store = user_store
        self.logger = logger
        self.username = username
        self.role = role
        self.build_ui()
        self.mainloop()

    def build_ui(self):
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)

        self.build_header(frame)

        tk.Label(frame, text=f"Logged in as: {self.username} ({self.role})", font=("Arial", 14)).pack(pady=5)
        tk.Label(frame, text=f"{self.role} Menu", font=("Arial", 18, "bold")).pack(pady=10)

        center = tk.Frame(frame)
        center.pack(pady=20)

        options = ROLE_MENU_OPTIONS.get(self.role, ["Logout"])
        for text in options:
            if self.role == "IT Department" and text == "Reset User Passwords":
                cmd = self.open_reset_password
            elif self.role == "IT Department" and text == "Unlock User Accounts":
                cmd = self.open_unlock_account
            elif self.role == "IT Department" and text == "View System Logs":
                cmd = self.view_logs
            elif text == "Logout":
                cmd = self.logout
            else:
                cmd = self.placeholder
            tk.Button(center, text=text, width=45, height=2, font=("Arial", 14), command=cmd).pack(pady=5)

    def open_reset_password(self):
        ResetPasswordWindow(self, self.user_store, self.logger, self.username)

    def open_unlock_account(self):
        UnlockAccountWindow(self, self.user_store, self.logger, self.username)

    def view_logs(self):
        win = tk.Toplevel(self)
        win.title("System Logs")
        win.geometry("800x500")
        tk.Label(win, text="System Logs", font=("Arial", 14, "bold")).pack(pady=5)
        txt = tk.Text(win, wrap="word", font=("Consolas", 10))
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("1.0", self.logger.get_all())
        txt.config(state="disabled")

    def placeholder(self):
        win = tk.Toplevel(self)
        win.title("Not Implemented Yet")
        win.geometry("400x200")
        tk.Label(win, text="This function will be implemented later.", font=("Arial", 12)).pack(pady=40)

    def logout(self):
        self.logger.log(f"Logout by user: {self.username}")
        self.destroy()
        LoginScreen(self.user_store, self.logger).mainloop()


# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":
    logger = Logger()
    store = UserStore(logger)
    app = LoginScreen(store, logger)
    app.mainloop()
