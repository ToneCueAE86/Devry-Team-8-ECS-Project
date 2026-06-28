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


class SysAdminMenu:
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
        # Updated by Tony Cuevas 6/20
        tk.Label(center,
                 text="SYSTEM ADMINISTRATION",
                 font=("Arial", 22, "bold"),
                 bg=BG, fg=FG).pack(pady=10)

        # System Admin Menu Buttons - Added "Create User Account" at top Tony Cuevas 6/25
        menu_items = [
            "Create User Account",
            "Reset User Passwords",
            "Unlock User Accounts",
            "View System Logs",
            "Run Diagnostics",
            "Backup/Restore Database"
        ]

        # Loop through items and assign the functional commands for management windows
        # Font size reduced from 18 to 14 Tony Cuevas 9/20
        # Button height reduced from 2 to 1 to fit screens cleanly Tony Cuevas 6/20
        # Padding lowered from 10 to 6 to stop layout overflow Tony Cuevas 6/20
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

            # Updated by Tony Cuevas 6/20
            tk.Button(center,
                      text=item,
                      font=("Arial", 14),
                      width=35,
                      height=1,
                      bg=BTN_BG,
                      fg=FG,
                      command=cmd).pack(pady=6)

        # Logout Button - Scaled down to match layout, positioned cleanly at the bottom Tony Cuevas 6/20
        # Updated by Tony Cuevas 6/20
        tk.Button(center,
                  text="Logout",
                  font=("Arial", 14),
                  width=20,
                  height=1,
                  bg=BTN_BG,
                  fg=FG,
                  command=self.logout).pack(pady=15)

    # Functional Account Creation Pop-up Window - Tony Cuevas 6/25
    def open_create_user_window(self):
        # Create a modal pop-up window
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

        # Email Field
        tk.Label(create_win, text="Email Address:", font=("Arial", 12), bg=BG, fg=FG).pack(pady=2)
        email_entry = tk.Entry(create_win, font=("Arial", 12), width=30)
        email_entry.pack(pady=5)

        # Phone Number Field
        tk.Label(create_win, text="Phone Number (e.g. 555-867-5309):", font=("Arial", 12), bg=BG, fg=FG).pack(pady=2)
        phone_entry = tk.Entry(create_win, font=("Arial", 12), width=30)
        phone_entry.pack(pady=5)

        # Equipment Training Level Dropdown
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
    # Updated by Tony Cuevas 6/20
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

    # Functional Unlock User Account Pop-up Window
    # Updated by Tony Cuevas 6/20
    def open_unlock_account_window(self):
        unlock_win = tk.Toplevel(self.root)
        unlock_win.title("Account Management - Unlock Account")
        unlock_win.geometry("450x350")
        unlock_win.configure(bg=BG)
        unlock_win.resizable(False, False)
        unlock_win.grab_set()

        tk.Label(unlock_win, text="UNLOCK USER ACCOUNT", font=("Arial", 16, "bold"), bg=BG, fg=FG).pack(pady=15)

        tk.Label(unlock_win, text="Target Username:", font=("Arial", 12), bg=BG, fg=FG).pack(pady=2)
        search_entry = tk.Entry(unlock_win, font=("Arial", 12), width=30)
        search_entry.pack(pady=5)

        status_label = tk.Label(unlock_win, text="Status: Search for a user first", font=("Arial", 12, "italic"),
                                bg=BG, fg="gray")
        status_label.pack(pady=15)

        action_frame = tk.Frame(unlock_win, bg=BG)
        action_frame.pack(pady=10)

        def search_user():
            target_user = search_entry.get().strip()
            if not target_user:
                messagebox.showerror("Error", "Please input a username to search.", parent=unlock_win)
                return

            import main
            if target_user in main.USERS:
                is_locked = main.USERS[target_user].get("status", "active") == "locked"
                if is_locked:
                    status_label.config(text="Status: LOCKED OUT", font=("Arial", 12, "bold"), fg="red")
                    unlock_btn.config(state="normal")
                else:
                    status_label.config(text="Status: ACTIVE (Normal)", font=("Arial", 12, "bold"), fg="green")
                    unlock_btn.config(state="disabled")
            else:
                status_label.config(text="Status: User Not Found", font=("Arial", 12, "italic"), fg="gray")
                unlock_btn.config(state="disabled")
                messagebox.showerror("Not Found", f"No user account named '{target_user}' exists.", parent=unlock_win)

        def execute_unlock():
            target_user = search_entry.get().strip()
            import main

            if target_user in main.USERS:
                main.USERS[target_user]["status"] = "active"
                if "attempts" in main.USERS[target_user]:
                    main.USERS[target_user]["attempts"] = 0

                messagebox.showinfo("Success", f"Account '{target_user}' has been unlocked successfully!",
                                    parent=unlock_win)
                unlock_win.destroy()

        tk.Button(unlock_win, text="Find Account", font=("Arial", 11), bg=BTN_BG, fg=FG, width=15,
                  command=search_user).pack(pady=5)

        unlock_btn = tk.Button(action_frame, text="Unlock Account", font=("Arial", 12, "bold"), bg=BTN_BG, fg=FG,
                               width=15, state="disabled", command=execute_unlock)
        unlock_btn.pack(side="left", padx=10)

        tk.Button(action_frame, text="Cancel", font=("Arial", 12), bg=BTN_BG, fg=FG, width=10,
                  command=unlock_win.destroy).pack(side="right", padx=10)

    # Functional View System Logs Pop-up Window
    # Updated by Tony Cuevas 6/20
    def open_system_logs_window(self):
        logs_win = tk.Toplevel(self.root)
        logs_win.title("System Maintenance - View Logs")
        logs_win.geometry("700x450")
        logs_win.configure(bg=BG)
        logs_win.grab_set()

        tk.Label(logs_win, text="SYSTEM AUDIT LOGS", font=("Arial", 16, "bold"), bg=BG, fg=FG).pack(pady=10)

        mock_logs = {
            "auth_log.txt": "[INFO] 2026-06-20 08:12:03 - User 'admin' logged in successfully.\n[WARN] 2026-06-20 09:44:12 - User 't_cuevas' locked out after 3 failed password attempts.\n[INFO] 2026-06-20 10:15:33 - Account 't_cuevas' unlocked by System Administrator.",
            "system_performance.txt": "[INFO] 2026-06-20 00:00:00 - Daily database sanity checks passed.\n[INFO] 2026-06-20 12:00:00 - Memory usage optimized. GC overhead: 1.2%.",
            "error_log.txt": "[ERROR] 2026-06-19 14:22:18 - Connection Timeout while connecting to local schema pool.\n[ERROR] 2026-06-20 11:05:42 - Top-level namespace exception avoided via deferred module loading runtime patch."
        }

        main_frame = tk.Frame(logs_win, bg=BG)
        main_frame.pack(fill="both", expand=True, padx=15, pady=5)

        list_frame = tk.Frame(main_frame, bg=BG)
        list_frame.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(list_frame, text="Select Log File:", font=("Arial", 11, "bold"), bg=BG, fg=FG).pack(anchor="w",
                                                                                                      pady=2)

        file_listbox = tk.Listbox(list_frame, font=("Arial", 10), width=22, selectmode="single",
                                  exportselection=False)
        file_listbox.pack(fill="both", expand=True)

        for file_name in mock_logs.keys():
            file_listbox.insert("end", file_name)

        text_frame = tk.Frame(main_frame, bg=BG)
        text_frame.pack(side="right", fill="both", expand=True)

        tk.Label(text_frame, text="Log File Contents:", font=("Arial", 11, "bold"), bg=BG, fg=FG).pack(anchor="w",
                                                                                                        pady=2)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        log_display = tk.Text(text_frame, font=("Courier New", 10), wrap="word", bg="white", fg="black",
                              yscrollcommand=scrollbar.set)
        log_display.pack(fill="both", expand=True)
        scrollbar.config(command=log_display.yview)

        log_display.insert("1.0", "Please select a log file from the left sidebar panel to preview system status events.")
        log_display.config(state="disabled")

        def on_file_select(event):
            selection = file_listbox.curselection()
            if not selection:
                return

            selected_file = file_listbox.get(selection)
            content = mock_logs.get(selected_file, "No data available.")

            log_display.config(state="normal")
            log_display.delete("1.0", "end")
            log_display.insert("1.0", content)
            log_display.config(state="disabled")

        file_listbox.bind("<<ListboxSelect>>", on_file_select)

        def export_log():
            selection = file_listbox.curselection()
            if not selection:
                messagebox.showwarning("No File Selected",
                                       "Please select an individual log file from the left sidebar menu list first before exporting.",
                                       parent=logs_win)
                return

            selected_file = file_listbox.get(selection)
            content = mock_logs.get(selected_file, "")

            export_path = filedialog.asksaveasfilename(
                parent=logs_win,
                initialfile=selected_file,
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )

            if export_path:
                try:
                    with open(export_path, "w", encoding="utf-8") as file:
                        file.write(content)
                    messagebox.showinfo("Export Successful", f"Log file content saved cleanly to:\n{export_path}",
                                        parent=logs_win)
                except Exception as e:
                    messagebox.showerror("Export Failed", f"An error occurred while saving the file:\n{str(e)}",
                                         parent=logs_win)

        bottom_frame = tk.Frame(logs_win, bg=BG)
        bottom_frame.pack(fill="x", pady=15)

        tk.Button(bottom_frame, text="Export File", font=("Arial", 11, "bold"), bg=BTN_BG, fg=FG, width=15,
                  command=export_log).pack(side="left", padx=30)
        tk.Button(bottom_frame, text="Close View", font=("Arial", 11), bg=BTN_BG, fg=FG, width=12,
                  command=logs_win.destroy).pack(side="right", padx=30)

    # Under Construction Message
    def under_construction(self):
        messagebox.showinfo(
            "Coming Soon",
            "This feature is under construction and not yet available."
        )

    # Logout → Back to Login Screen
    def logout(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Safely import main locally to avoid a circular dependency crash Tony Cuevas 6/20, Moved the Imports: import main is now strictly inside the scope of the logout function and the build_header function.
        # Updated by Tony Cuevas 6/20
        import main
        main.LoginWindow(self.root)