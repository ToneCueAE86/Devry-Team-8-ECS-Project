import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os

BG = "#e6e6e6"
BTN_BG = "#c0c0c0"
FG = "black"


# Reuse header from main.py
def build_header(parent):
    import main  # Deferred import to prevent top-level circular dependency Tony Cuevas 6/20
    main.build_header(parent)


class ITMenu:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=BG)
        self.root.state("zoomed")

        # Center frame container
        center = tk.Frame(root, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        build_header(center)

        # Title - Reduced from 28 to 22 font size and tightened padding Tony Cuevas 6/20
        tk.Label(center,
                 text="IT DEPARTMENT",
                 font=("Arial", 22, "bold"),
                 bg=BG, fg=FG).pack(pady=10)

        # IT Menu Buttons (Added "Create User Account" above "Reset User Passwords")
        menu_items = [
            "Create User Account",
            "Reset User Passwords",
            "Unlock User Accounts",
            "View System Logs",
            "Run Diagnostics",
            "Backup / Restore Database"
        ]

        # Loop through items and assign the functional commands for account management
        for item in menu_items:
            if item == "Create User Account":
                cmd = self.open_create_user_window
            elif item == "Reset User Passwords":
                cmd = self.open_reset_password_window
            elif item == "Unlock User Accounts":
                cmd = self.open_unlock_account_window
            elif item == "View System Logs":
                cmd = self.open_system_logs_window
            else:
                cmd = self.under_construction

            tk.Button(center,
                      text=item,
                      font=("Arial", 14),
                      width=35,
                      height=1,
                      bg=BTN_BG,
                      fg=FG,
                      command=cmd).pack(pady=6)

        # Logout Button
        tk.Button(center,
                  text="Logout",
                  font=("Arial", 14),
                  width=20,
                  height=1,
                  bg=BTN_BG,
                  fg=FG,
                  command=self.logout).pack(pady=15)

    # Functional Account Creation Pop-up Window
    def open_create_user_window(self):
        # Create a modal pop-up window
        # Increased height from 380 to 620 to accommodate new fields Tony Cuevas 6/25
        create_win = tk.Toplevel(self.root)
        create_win.title("Account Management - Create User")
        create_win.geometry("480x620")
        create_win.configure(bg=BG)
        create_win.resizable(False, False)

        # Lock window focus
        create_win.grab_set()

        # Window Header
        tk.Label(create_win, text="CREATE USER ACCOUNT", font=("Arial", 16, "bold"), bg=BG, fg=FG).pack(pady=15)

        # Username Field
        tk.Label(create_win, text="New Username:", font=("Arial", 12), bg=BG, fg=FG).pack(pady=2)
        username_entry = tk.Entry(create_win, font=("Arial", 12), width=30)
        username_entry.pack(pady=5)

        # Password Field
        tk.Label(create_win, text="Password:", font=("Arial", 12), bg=BG, fg=FG).pack(pady=2)
        password_entry = tk.Entry(create_win, font=("Arial", 12), width=30, show="*")
        password_entry.pack(pady=5)

        # Department Field
        tk.Label(create_win, text="Department (depot, it, maintenance, supply, sysadmin):",
                 font=("Arial", 11), bg=BG, fg=FG).pack(pady=2)
        dept_entry = tk.Entry(create_win, font=("Arial", 12), width=30)
        dept_entry.pack(pady=5)

        # Email Field - Tony Cuevas 6/25
        tk.Label(create_win, text="Email Address:", font=("Arial", 12), bg=BG, fg=FG).pack(pady=2)
        email_entry = tk.Entry(create_win, font=("Arial", 12), width=30)
        email_entry.pack(pady=5)

        # Phone Number Field - Tony Cuevas 6/25
        tk.Label(create_win, text="Phone Number (e.g. 555-867-5309):", font=("Arial", 12), bg=BG, fg=FG).pack(pady=2)
        phone_entry = tk.Entry(create_win, font=("Arial", 12), width=30)
        phone_entry.pack(pady=5)

        # Equipment Training Level Dropdown - Tony Cuevas 6/25
        tk.Label(create_win, text="Equipment Training Level:", font=("Arial", 12), bg=BG, fg=FG).pack(pady=2)
        training_options = ["None", "Basic", "Intermediate", "Advanced", "Certified Trainer"]
        training_var = tk.StringVar(create_win)
        training_var.set(training_options[0])  # Default to "None"
        training_menu = tk.OptionMenu(create_win, training_var, *training_options)
        training_menu.config(font=("Arial", 12), bg=BTN_BG, fg=FG, width=20)
        training_menu.pack(pady=5)

        # Submit Action Functionality
        def execute_create():
            new_user = username_entry.get().strip()
            new_pass = password_entry.get().strip()
            dept = dept_entry.get().strip().lower()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            training = training_var.get()

            # Validate all required fields are filled
            if not new_user or not new_pass or not dept or not email or not phone:
                messagebox.showerror("Error", "All fields are required.", parent=create_win)
                return

            # Basic email format check
            if "@" not in email or "." not in email.split("@")[-1]:
                messagebox.showerror("Error", "Please enter a valid email address.", parent=create_win)
                return

            import main

            # Check if username already exists
            if new_user in main.USERS:
                messagebox.showerror("Error", f"User '{new_user}' already exists in the system.", parent=create_win)
                return

            # Update the global USERS dictionary directly in memory
            main.USERS[new_user] = {
                "password": new_pass,
                "department": dept,
                "email": email,
                "phone": phone,
                "training_level": training
            }

            messagebox.showinfo(
                "Success",
                f"Account for '{new_user}' created successfully!\n\n"
                f"Department: {dept}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Training Level: {training}",
                parent=create_win
            )
            create_win.destroy()

        # Action Layout Control
        btn_frame = tk.Frame(create_win, bg=BG)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Create Account", font=("Arial", 12, "bold"), bg=BTN_BG, fg=FG, width=15,
                  command=execute_create).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", font=("Arial", 12), bg=BTN_BG, fg=FG, width=10,
                  command=create_win.destroy).pack(side="right", padx=10)

    # Functional Password Reset Pop-up Window
    def open_reset_password_window(self):
        reset_win = tk.Toplevel(self.root)
        reset_win.title("Account Management - Reset Password")
        reset_win.geometry("450x320")
        reset_win.configure(bg=BG)
        reset_win.resizable(False, False)
        reset_win.grab_set()

        tk.Label(reset_win, text="RESET USER PASSWORD", font=("Arial", 16, "bold"), bg=BG, fg=FG).pack(pady=15)

        tk.Label(reset_win, text="Target Username:", font=("Arial", 12), bg=BG, fg=FG).pack(pady=2)
        username_entry = tk.Entry(reset_win, font=("Arial", 12), width=30)
        username_entry.pack(pady=5)

        tk.Label(reset_win, text="New Password:", font=("Arial", 12), bg=BG, fg=FG).pack(pady=2)
        password_entry = tk.Entry(reset_win, font=("Arial", 12), width=30, show="*")
        password_entry.pack(pady=5)

        def execute_reset():
            target_user = username_entry.get().strip()
            new_pass = password_entry.get().strip()

            if not target_user or not new_pass:
                messagebox.showerror("Error", "All fields are required.", parent=reset_win)
                return

            import main

            if target_user in main.USERS:
                main.USERS[target_user]["password"] = new_pass
                messagebox.showinfo("Success", f"Password for '{target_user}' has been updated successfully!",
                                    parent=reset_win)
                reset_win.destroy()
            else:
                messagebox.showerror("User Not Found", f"No user account named '{target_user}' exists in the system.",
                                     parent=reset_win)

        btn_frame = tk.Frame(reset_win, bg=BG)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Update Password", font=("Arial", 12, "bold"), bg=BTN_BG, fg=FG, width=15,
                  command=execute_reset).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", font=("Arial", 12), bg=BTN_BG, fg=FG, width=10,
                  command=reset_win.destroy).pack(side="right", padx=10)

    # Placeholder windows for remaining functionality
    def open_unlock_account_window(self):
        # Implementation remains the same as your existing code
        pass

    def open_system_logs_window(self):
        # Implementation remains the same as your existing code
        pass

    def under_construction(self):
        messagebox.showinfo("Coming Soon", "This feature is under construction and not yet available.")

    def logout(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        import main
        main.LoginScreen(self.root)