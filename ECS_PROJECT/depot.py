import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from employee_profile_window import EmployeeProfileWindow
import json
import os

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import json
import os

BG = "#e6e6e6"
BTN_BG = "#c0c0c0"
FG = "black"


# ---------------------------------------------------------
# HEADER (LOGO + DATE/TIME)
# ---------------------------------------------------------
def build_header(parent):
    header = tk.Frame(parent, bg=BG)
    header.pack(pady=5)

    canvas = tk.Canvas(header, width=160, height=160,
                       bg=BG, highlightthickness=0)
    canvas.pack()

    canvas.create_oval(10, 10, 150, 150, outline="black", width=3)
    canvas.create_text(80, 55, text="GB",
                       fill="black", font=("Arial", 30, "bold"))
    canvas.create_text(80, 100, text="MANUFACTURING",
                       fill="black", font=("Arial", 12, "bold"))

    now = datetime.now().strftime("%A, %B %d, %Y | %I:%M %p")
    tk.Label(header,
             text=now,
             font=("Arial", 11),
             bg=BG, fg=FG).pack(pady=2)


# ---------------------------------------------------------
# DEPOT MENU
# ---------------------------------------------------------
class DepotMenu:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=BG)
        self.root.state("zoomed")

        center = tk.Frame(root, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        build_header(center)

        tk.Label(center,
                 text="DEPOT DEPARTMENT",
                 font=("Arial", 28, "bold"),
                 bg=BG, fg=FG).pack(pady=20)

        # Functional button
        tk.Button(center,
                  text="Process Equipment Checkout",
                  font=("Arial", 18),
                  width=35,
                  height=2,
                  bg=BTN_BG,
                  fg=FG,
                  command=self.open_verification).pack(pady=10)

        # Other menu items – show "under construction"
        menu_items = [
            "Process Equipment Return",
            "Update Equipment Availability",
            "Mark Equipment Lost / Damaged",
            "View All Checked-Out Equipment",
            "View Overdue Equipment"
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

        tk.Button(center,
                  text="Logout",
                  font=("Arial", 18),
                  width=20,
                  height=1,
                  bg=BTN_BG,
                  fg=FG,
                  command=self.under_construction).pack(pady=25)

    def open_verification(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        EmployeeVerificationWindow(self.root)

    def under_construction(self):
        messagebox.showinfo(
            "Coming Soon",
            "This feature is under construction and not yet available."
        )



    def exit_to_login(self):
        try:
            from main import LoginWindow
            for widget in self.root.winfo_children():
                widget.destroy()
            LoginWindow(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Could not return to login:\n{e}")


# ---------------------------------------------------------
# EMPLOYEE VERIFICATION WINDOW
# ---------------------------------------------------------
class EmployeeVerificationWindow:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=BG)

        center = tk.Frame(root, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        build_header(center)

        tk.Label(center,
                 text="EMPLOYEE VERIFICATION",
                 font=("Arial", 28, "bold"),
                 bg=BG, fg=FG).pack(pady=20)

        tk.Label(center, text="First Name:",
                 font=("Arial", 16), bg=BG, fg=FG).pack()
        self.first_name_entry = tk.Entry(center, font=("Arial", 16), width=30)
        self.first_name_entry.pack(pady=5)

        tk.Label(center, text="Last Name:",
                 font=("Arial", 16), bg=BG, fg=FG).pack()
        self.last_name_entry = tk.Entry(center, font=("Arial", 16), width=30)
        self.last_name_entry.pack(pady=5)

        tk.Label(center, text="Employee ID:",
                 font=("Arial", 16), bg=BG, fg=FG).pack()
        self.employee_id_entry = tk.Entry(center, font=("Arial", 16), width=30)
        self.employee_id_entry.pack(pady=5)

        btn_frame = tk.Frame(center, bg=BG)
        btn_frame.pack(pady=25)

        tk.Button(btn_frame,
                  text="Verify Employee",
                  font=("Arial", 16),
                  width=18,
                  bg=BTN_BG, fg=FG,
                  command=self.verify_employee).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame,
                  text="Cancel",
                  font=("Arial", 16),
                  width=12,
                  bg=BTN_BG, fg=FG,
                  command=self.go_back).grid(row=0, column=1, padx=10)

    def verify_employee(self):
        first = self.first_name_entry.get().strip().lower()
        last = self.last_name_entry.get().strip().lower()
        emp_id = self.employee_id_entry.get().strip().upper()

        json_path = os.path.join(
            os.path.dirname(__file__),
            "data",
            "borrower_registry.json"
        )

        try:
            with open(json_path, "r") as f:
                borrowers = json.load(f)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not load borrower_registry.json\n\n{e}"
            )
            return

        match = None
        for b in borrowers:
            if (b["first_name"].lower() == first and
                b["last_name"].lower() == last and
                b["employee_id"].upper() == emp_id):
                match = b
                break

        if not match:
            messagebox.showerror("Not Found", "Employee not found.")
            return

        status = match["status"].lower()

        if status == "terminated":
            messagebox.showerror(
                "Access Denied",
                "This employee is TERMINATED and cannot borrow equipment."
            )
            return

        if status == "suspended":
            messagebox.showerror(
                "Access Denied",
                "This employee is SUSPENDED and cannot borrow equipment."
            )
            return

        if status == "restricted":
            messagebox.showwarning(
                "Restricted",
                "This employee is RESTRICTED. Supervisor approval required."
            )

        for widget in self.root.winfo_children():
            widget.destroy()
        EmployeeProfileWindow(self.root, match)

    def go_back(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        DepotMenu(self.root)


# ---------------------------------------------------------
# EMPLOYEE PROFILE WINDOW
# ---------------------------------------------------------
class EmployeeProfileWindow:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.root.configure(bg=BG)

        center = tk.Frame(root, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        build_header(center)

        tk.Label(center,
                 text="EMPLOYEE PROFILE",
                 font=("Arial", 15, "bold"),
                 bg=BG, fg=FG).pack(pady=10)

        # ---------------- PHOTO BOX ----------------
        photo_box = tk.Frame(center, width=150, height=150,
                             bg="white", highlightbackground="black",
                             highlightthickness=2)
        photo_box.pack(pady=5)
        tk.Label(photo_box,
                 text="PHOTO",
                 font=("Arial", 10, "bold"),
                 bg="white").place(relx=0.5, rely=0.5, anchor="center")

        # ---------------- 3-COLUMN SECTION ----------------
        columns = tk.Frame(center, bg=BG)
        columns.pack(pady=10, fill="x")

        col1 = tk.Frame(columns, bg=BG)
        col2 = tk.Frame(columns, bg=BG)
        col3 = tk.Frame(columns, bg=BG)

        col1.pack(side="left", expand=True, fill="both", padx=10)
        col2.pack(side="left", expand=True, fill="both", padx=10)
        col3.pack(side="left", expand=True, fill="both", padx=10)

        # Helper function for rows
        def add_row(parent, label, value):
            row = tk.Frame(parent, bg=BG)
            row.pack(anchor="w", pady=1)
            tk.Label(row, text=f"{label}:",
                     font=("Arial", 12, "bold"),
                     bg=BG, fg=FG).pack(side="left")
            tk.Label(row, text=f" {value}",
                     font=("Arial", 12),
                     bg=BG, fg=FG).pack(side="left")

        # ---------------- COLUMN 1: IDENTITY ----------------
        tk.Label(col1, text="Identity Information",
                 font=("Arial", 14, "bold"), bg=BG).pack(anchor="w")
        add_row(col1, "First Name", data["first_name"])
        add_row(col1, "Last Name", data["last_name"])
        add_row(col1, "Employee ID", data["employee_id"])
        add_row(col1, "Job Title", data["job_title"])
        add_row(col1, "Department", data["department"])
        add_row(col1, "Status", data["status"])

        # ---------------- COLUMN 2: CONTACT ----------------
        tk.Label(col2, text="Contact Information",
                 font=("Arial", 14, "bold"), bg=BG).pack(anchor="w")
        add_row(col2, "Phone Number", data["phone"])
        add_row(col2, "Email Address", data["email"])
        add_row(col2, "Work Location", data["work_location"])

        # ---------------- COLUMN 3: QUALIFICATIONS ----------------
        tk.Label(col3, text="Qualifications",
                 font=("Arial", 14, "bold"), bg=BG).pack(anchor="w")

        tk.Label(col3, text="Specializations:",
                 font=("Arial", 12, "bold"), bg=BG).pack(anchor="w")
        for spec in data["specializations"]:
            tk.Label(col3, text=f"• {spec}",
                     font=("Arial", 12), bg=BG).pack(anchor="w")

        tk.Label(col3, text="Certifications:",
                 font=("Arial", 12, "bold"), bg=BG).pack(anchor="w", pady=(10, 0))
        for cert in data["certifications"]:
            tk.Label(col3,
                     text=f"• {cert['name']} — Issued: {cert['issued']}",
                     font=("Arial", 12), bg=BG).pack(anchor="w")

        # ---------------- SUPERVISOR INFO (FULL WIDTH) ----------------
        sup_frame = tk.Frame(center, bg=BG)
        sup_frame.pack(pady=10, fill="x")

        tk.Label(sup_frame, text="Supervisor Information",
                 font=("Arial", 14, "bold"), bg=BG).pack(anchor="w")
        add_row(sup_frame, "Supervisor Name", data["supervisor_name"])
        add_row(sup_frame, "Supervisor Phone", data["supervisor_phone"])
        add_row(sup_frame, "Supervisor Email", data["supervisor_email"])

        # ---------------- NOTES (FULL WIDTH) ----------------
        notes_frame = tk.Frame(center, bg=BG)
        notes_frame.pack(pady=10, fill="x")

        tk.Label(notes_frame, text="Notes",
                 font=("Arial", 14, "bold"), bg=BG).pack(anchor="w")
        tk.Label(notes_frame,
                 text=data["notes"] if data["notes"] else "(No notes on file)",
                 font=("Arial", 12), bg=BG).pack(anchor="w")

        # ---------------- BUTTONS ----------------
        btn_frame = tk.Frame(center, bg=BG)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame,
                  text="Proceed to Checkout",
                  font=("Arial", 14),
                  width=25,
                  bg=BTN_BG, fg=FG,
                  command=self.proceed).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame,
                  text="Cancel",
                  font=("Arial", 14),
                  width=12,
                  bg=BTN_BG, fg=FG,
                  command=self.cancel).grid(row=0, column=1, padx=10)

    def proceed(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        CheckoutFormWindow(self.root, self.data)

    def cancel(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        DepotMenu(self.root)



# ---------------------------------------------------------
# CHECKOUT FORM WINDOW
# ---------------------------------------------------------
class CheckoutFormWindow:
    def __init__(self, root, employee):
        self.root = root
        self.employee = employee
        self.root.configure(bg=BG)

        # Hard-coded equipment list
        self.load_equipment_db()

        self.checkout_items = []
        self.filtered_equipment = list(self.equipment)

        main = tk.Frame(root, bg=BG)
        main.place(relx=0.5, rely=0.03, anchor="n")

        build_header(main)

        tk.Label(main,
                 text="EQUIPMENT CHECKOUT FORM",
                 font=("Arial", 26, "bold"),
                 bg=BG, fg=FG).pack(pady=10)

        # ---------------- EMPLOYEE INFO ----------------
        info = tk.Frame(main, bg=BG)
        info.pack(pady=5, fill="x")

        tk.Label(info, text="Employee Information",
                 font=("Arial", 18, "bold"),
                 bg=BG, fg=FG).pack(anchor="w", pady=(0, 5))

        left = tk.Frame(info, bg=BG)
        right = tk.Frame(info, bg=BG)
        left.pack(side="left", anchor="n", padx=10)
        right.pack(side="right", anchor="n", padx=10)

        def row(parent, label, value):
            r = tk.Frame(parent, bg=BG)
            r.pack(anchor="w")
            tk.Label(r, text=f"{label}: ",
                     font=("Arial", 14, "bold"),
                     bg=BG).pack(side="left")
            tk.Label(r, text=value,
                     font=("Arial", 14),
                     bg=BG).pack(side="left")

        full_name = f"{employee['first_name']} {employee['last_name']}"
        row(left, "Name", full_name)
        row(left, "Employee ID", employee["employee_id"])
        row(left, "Phone", employee["phone"])
        row(left, "Email", employee["email"])
        row(left, "Work Location", employee["work_location"])

        row(right, "Supervisor", employee["supervisor_name"])
        row(right, "Sup. Phone", employee["supervisor_phone"])
        row(right, "Sup. Email", employee["supervisor_email"])

        # ---------------- DATES ----------------
        date_frame = tk.Frame(main, bg=BG)
        date_frame.pack(pady=10, fill="x")

        tk.Label(date_frame, text="Pickup Date:",
                 font=("Arial", 14, "bold"), bg=BG).grid(row=0, column=0, sticky="w", padx=10)
        self.pickup_entry = tk.Entry(date_frame, font=("Arial", 14), width=12)
        self.pickup_entry.grid(row=0, column=1, padx=5)
        tk.Button(date_frame, text="📅", font=("Arial", 12),
                  command=lambda: self.open_calendar(self.pickup_entry)).grid(row=0, column=2)

        tk.Label(date_frame, text="Return Date:",
                 font=("Arial", 14, "bold"), bg=BG).grid(row=0, column=3, sticky="w", padx=30)
        self.return_entry = tk.Entry(date_frame, font=("Arial", 14), width=12)
        self.return_entry.grid(row=0, column=4, padx=5)
        tk.Button(date_frame, text="📅", font=("Arial", 12),
                  command=lambda: self.open_calendar(self.return_entry)).grid(row=0, column=5)

        # ---------------- SEARCH EQUIPMENT ----------------
        eq_frame = tk.Frame(main, bg=BG)
        eq_frame.pack(pady=10, fill="x")

        search_row = tk.Frame(eq_frame, bg=BG)
        search_row.pack(anchor="w", pady=5)

        tk.Label(search_row, text="Search Equipment:",
                 font=("Arial", 14, "bold"), bg=BG).pack(side="left")

        self.search_entry = tk.Entry(search_row, font=("Arial", 14), width=40)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        self.equipment_var = tk.StringVar(value="")
        self.dropdown_btn = tk.Menubutton(search_row, text="▼", font=("Arial", 12), relief="raised")
        self.dropdown_menu = tk.Menu(self.dropdown_btn, tearoff=0)
        self.dropdown_btn.config(menu=self.dropdown_menu)
        self.dropdown_btn.pack(side="left")

        # Notes
        notes_row = tk.Frame(eq_frame, bg=BG)
        notes_row.pack(anchor="w", pady=(8, 0))

        tk.Label(notes_row, text="Notes / Comments:",
                 font=("Arial", 14, "bold"), bg=BG).pack(side="left")
        self.notes_entry = tk.Entry(notes_row, font=("Arial", 14), width=50)
        self.notes_entry.pack(side="left", padx=5)

        # ---------------- CHECKOUT LIST ----------------
        list_frame = tk.Frame(main, bg=BG)
        list_frame.pack(pady=10)

        tk.Label(list_frame, text="Checkout List",
                 font=("Arial", 18, "bold"), bg=BG).pack(anchor="w")

        self.tree = ttk.Treeview(list_frame,
                                 columns=("id", "desc", "notes", "qty"),
                                 show="headings",
                                 height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("desc", text="Description")
        self.tree.heading("notes", text="Notes")
        self.tree.heading("qty", text="Qty")

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("desc", width=220, anchor="w")
        self.tree.column("notes", width=260, anchor="w")
        self.tree.column("qty", width=60, anchor="center")

        self.tree.pack()

        btns = tk.Frame(list_frame, bg=BG)
        btns.pack(pady=5)

        tk.Button(btns, text="+", width=5, font=("Arial", 14),
                  command=self.increase_qty).pack(side="left", padx=5)
        tk.Button(btns, text="-", width=5, font=("Arial", 14),
                  command=self.decrease_qty).pack(side="left", padx=5)
        tk.Button(btns, text="X", width=5, font=("Arial", 14),
                  command=self.remove_item).pack(side="left", padx=5)

        tk.Button(list_frame, text="Clear All",
                  font=("Arial", 14), bg=BTN_BG,
                  command=self.clear_all).pack(pady=5)

        bottom = tk.Frame(main, bg=BG)
        bottom.pack(pady=15, fill="x")

        tk.Button(bottom, text="Cancel",
                  font=("Arial", 16), width=12,
                  bg=BTN_BG, command=self.cancel).pack(side="left", padx=20)

        tk.Button(bottom, text="Proceed Checkout",
                  font=("Arial", 16), width=20,
                  bg=BTN_BG, command=self.proceed).pack(side="right", padx=20)

        self.populate_dropdown(self.filtered_equipment)

    # ---------------- EQUIPMENT DB ----------------
    def load_equipment_db(self):
        self.equipment = [
            {
                "id": "EQ001",
                "name": "Cordless Drill",
                "category": "Power Tools",
                "subcategory": "Drills",
                "trade": "Carpentry",
                "certification_required": "Basic Power Tools",
                "quantity": 12,
                "location": "Supply Room A",
                "aisle": "A1",
                "shelf": "S1",
                "row": "R1",
                "condition": "Good",
                "status": "Operational",
                "comments": "Frequently used. Inspect monthly.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ002",
                "name": "Impact Driver",
                "category": "Power Tools",
                "subcategory": "Drivers",
                "trade": "Carpentry",
                "certification_required": "Basic Power Tools",
                "quantity": 8,
                "location": "Supply Room A",
                "aisle": "A1",
                "shelf": "S2",
                "row": "R1",
                "condition": "Fair",
                "status": "Under Repair",
                "comments": "Reported torque issue.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ003",
                "name": "Hammer Drill",
                "category": "Power Tools",
                "subcategory": "Drills",
                "trade": "Electrician",
                "certification_required": "Electrical Safety",
                "quantity": 5,
                "location": "Supply Room A",
                "aisle": "A1",
                "shelf": "S3",
                "row": "R1",
                "condition": "Poor",
                "status": "Broken",
                "comments": "Motor failure. Needs replacement.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ004",
                "name": "Angle Grinder",
                "category": "Power Tools",
                "subcategory": "Grinders",
                "trade": "Metalwork",
                "certification_required": "Basic Power Tools",
                "quantity": 6,
                "location": "Supply Room B",
                "aisle": "B1",
                "shelf": "S1",
                "row": "R2",
                "condition": "Good",
                "status": "Operational",
                "comments": "New discs added recently.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ005",
                "name": "Circular Saw",
                "category": "Power Tools",
                "subcategory": "Saws",
                "trade": "Carpentry",
                "certification_required": "Basic Power Tools",
                "quantity": 7,
                "location": "Supply Room B",
                "aisle": "B1",
                "shelf": "S2",
                "row": "R2",
                "condition": "Good",
                "status": "Operational",
                "comments": "Blade replaced last week.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ006",
                "name": "Sledgehammer",
                "category": "Hand Tools",
                "subcategory": "Hammers",
                "trade": "General Labor",
                "certification_required": "None",
                "quantity": 10,
                "location": "Supply Room C",
                "aisle": "C1",
                "shelf": "S1",
                "row": "R3",
                "condition": "Good",
                "status": "Operational",
                "comments": "Handles inspected quarterly.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ007",
                "name": "Pipe Wrench",
                "category": "Hand Tools",
                "subcategory": "Wrenches",
                "trade": "Plumbing",
                "certification_required": "None",
                "quantity": 14,
                "location": "Supply Room C",
                "aisle": "C1",
                "shelf": "S2",
                "row": "R3",
                "condition": "Fair",
                "status": "Operational",
                "comments": "Some wear on teeth.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ008",
                "name": "Adjustable Wrench",
                "category": "Hand Tools",
                "subcategory": "Wrenches",
                "trade": "General Labor",
                "certification_required": "None",
                "quantity": 20,
                "location": "Supply Room C",
                "aisle": "C1",
                "shelf": "S3",
                "row": "R3",
                "condition": "Good",
                "status": "Operational",
                "comments": "No issues reported.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ009",
                "name": "Socket Set",
                "category": "Hand Tools",
                "subcategory": "Sockets",
                "trade": "Mechanic",
                "certification_required": "None",
                "quantity": 9,
                "location": "Supply Room C",
                "aisle": "C2",
                "shelf": "S1",
                "row": "R3",
                "condition": "Good",
                "status": "Operational",
                "comments": "Complete set.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ010",
                "name": "Torque Wrench",
                "category": "Hand Tools",
                "subcategory": "Wrenches",
                "trade": "Mechanic",
                "certification_required": "None",
                "quantity": 4,
                "location": "Supply Room C",
                "aisle": "C2",
                "shelf": "S2",
                "row": "R3",
                "condition": "Needs Calibration",
                "status": "Needs Inspection",
                "comments": "Calibration overdue.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ011",
                "name": "Portable Air Compressor",
                "category": "Machinery",
                "subcategory": "Compressors",
                "trade": "HVAC",
                "certification_required": "Machinery Operation",
                "quantity": 3,
                "location": "Equipment Bay 1",
                "aisle": "E1",
                "shelf": "S1",
                "row": "R4",
                "condition": "Fair",
                "status": "Under Repair",
                "comments": "Leak detected in hose.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ012",
                "name": "Hydraulic Jack",
                "category": "Machinery",
                "subcategory": "Lifting",
                "trade": "Mechanic",
                "certification_required": "Machinery Operation",
                "quantity": 5,
                "location": "Equipment Bay 1",
                "aisle": "E1",
                "shelf": "S2",
                "row": "R4",
                "condition": "Good",
                "status": "Operational",
                "comments": "Inspected last month.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ013",
                "name": "Generator 5kW",
                "category": "Machinery",
                "subcategory": "Generators",
                "trade": "Electrician",
                "certification_required": "Electrical Safety",
                "quantity": 2,
                "location": "Equipment Bay 2",
                "aisle": "E2",
                "shelf": "S1",
                "row": "R4",
                "condition": "Poor",
                "status": "Out of Service",
                "comments": "Engine failure reported.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ014",
                "name": "Extension Cord 50ft",
                "category": "Electrical",
                "subcategory": "Cables",
                "trade": "Electrician",
                "certification_required": "None",
                "quantity": 18,
                "location": "Supply Room D",
                "aisle": "D1",
                "shelf": "S1",
                "row": "R5",
                "condition": "Good",
                "status": "Operational",
                "comments": "No issues.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ015",
                "name": "LED Work Light",
                "category": "Electrical",
                "subcategory": "Lighting",
                "trade": "Electrician",
                "certification_required": "None",
                "quantity": 11,
                "location": "Supply Room D",
                "aisle": "D1",
                "shelf": "S2",
                "row": "R5",
                "condition": "Good",
                "status": "Operational",
                "comments": "Bulbs replaced recently.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ016",
                "name": "Voltage Tester",
                "category": "Electrical",
                "subcategory": "Testers",
                "trade": "Electrician",
                "certification_required": "Electrical Safety",
                "quantity": 6,
                "location": "Supply Room D",
                "aisle": "D1",
                "shelf": "S3",
                "row": "R5",
                "condition": "Fair",
                "status": "Needs Inspection",
                "comments": "Accuracy inconsistent.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ017",
                "name": "Safety Helmet",
                "category": "PPE",
                "subcategory": "Head Protection",
                "trade": "Safety",
                "certification_required": "PPE Training",
                "quantity": 24,
                "location": "Safety Locker",
                "aisle": "SL1",
                "shelf": "S1",
                "row": "R6",
                "condition": "Good",
                "status": "Operational",
                "comments": "New batch.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            },
            {
                "id": "EQ018",
                "name": "Safety Goggles",
                "category": "PPE",
                "subcategory": "Eye Protection",
                "trade": "Safety",
                "certification_required": "PPE Training",
                "quantity": 30,
                "location": "Safety Locker",
                "aisle": "SL1",
                "shelf": "S2",
                "row": "R6",
                "condition": "Good",
                "status": "Operational",
                "comments": "No issues.",
                "borrower": "",
                "borrower_id": "",
                "borrow_date": "",
                "return_date": ""
            }
        ]

    # ---------------- CALENDAR ----------------
    def open_calendar(self, target_entry):
        import calendar
        from datetime import date

        top = tk.Toplevel(self.root)
        top.title("Select Date")
        top.geometry("260x260")
        top.resizable(False, False)

        today = date.today()
        year = today.year
        month = today.month

        tk.Label(top, text=f"{today.strftime('%B %Y')}",
                 font=("Arial", 14, "bold")).pack(pady=5)

        cal_frame = tk.Frame(top)
        cal_frame.pack()

        month_days = calendar.monthcalendar(year, month)

        for week in month_days:
            row = tk.Frame(cal_frame)
            row.pack()
            for day in week:
                if day == 0:
                    tk.Label(row, text="   ", width=3).pack(side="left")
                else:
                    tk.Button(
                        row,
                        text=str(day),
                        width=3,
                        command=lambda d=day: self.set_date(target_entry, d, top)
                    ).pack(side="left")

    def set_date(self, entry, day, window):
        from datetime import date
        today = date.today()
        entry.delete(0, "end")
        entry.insert(0, f"{today.year}-{today.month:02d}-{day:02d}")
        window.destroy()

    # ---------------- SEARCH + DROPDOWN ----------------
    def populate_dropdown(self, items):
        self.dropdown_menu.delete(0, "end")
        for eq in items:
            label = f"{eq['id']} – {eq['name']}"
            self.dropdown_menu.add_command(
                label=label,
                command=lambda v=label: self.add_item_from_label(v)
            )

    def on_search_change(self, event=None):
        query = self.search_entry.get().strip().lower()
        self.filtered_equipment = [
            eq for eq in self.equipment
            if query in eq["id"].lower() or query in eq["name"].lower()
        ]
        self.populate_dropdown(self.filtered_equipment)

    # ---------------- ADD ITEM ----------------
    def add_item_from_label(self, label):
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, label)

        eq_id = label.split(" – ")[0]
        eq = next((e for e in self.equipment if e["id"] == eq_id), None)

        if not eq:
            return

        # Status checks
        if eq["status"] in ["Broken", "Out of Service", "Under Repair", "Needs Inspection"]:
            messagebox.showerror("Unavailable",
                                 f"{eq['name']} is {eq['status']}.\nComments: {eq['comments']}")
            return

        # Certification check
        cert_req = eq.get("certification_required", "None")
        emp_certs = [c["name"] for c in self.employee.get("certifications", [])]
        if cert_req != "None" and cert_req not in emp_certs:
            messagebox.showerror("Not Authorized",
                                 f"This equipment requires: {cert_req}")
            return

        # Quantity check
        if eq["quantity"] <= 0:
            messagebox.showerror("No Stock",
                                 f"No available quantity for {eq['name']}.")
            return

        notes = self.notes_entry.get().strip()
        pickup = self.pickup_entry.get().strip()
        ret = self.return_entry.get().strip()

        item = {
            "id": eq["id"],
            "name": eq["name"],
            "notes": notes,
            "qty": 1,
            "pickup": pickup,
            "return": ret
        }

        self.checkout_items.append(item)
        self.notes_entry.delete(0, "end")
        self.refresh_list()

    # ---------------- LIST OPS ----------------
    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.checkout_items:
            self.tree.insert("", "end",
                             values=(item["id"], item["name"], item["notes"], item["qty"]))

    def get_selected_index(self):
        sel = self.tree.selection()
        if not sel:
            return None
        row = self.tree.item(sel[0])["values"]
        eq_id = row[0]
        for i, it in enumerate(self.checkout_items):
            if it["id"] == eq_id:
                return i
        return None

    def increase_qty(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        self.checkout_items[idx]["qty"] += 1
        self.refresh_list()

    def decrease_qty(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        if self.checkout_items[idx]["qty"] > 1:
            self.checkout_items[idx]["qty"] -= 1
            self.refresh_list()

    def remove_item(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        del self.checkout_items[idx]
        self.refresh_list()

    def clear_all(self):
        self.checkout_items = []
        self.refresh_list()

    # ---------------- NAVIGATION ----------------
    def proceed(self):
        if not self.checkout_items:
            messagebox.showerror("Error", "No items in checkout list.")
            return

        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Open the Final Confirmation Window
        FinalConfirmationWindow(self.root, self.employee, self.checkout_items)

    def cancel(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        DepotMenu(self.root)

# ---------------------------------------------------------
# FINAL CONFIRMATION / RECEIPT WINDOW
# ---------------------------------------------------------
class FinalConfirmationWindow:
    def __init__(self, root, employee, checkout_items):
        # Store references
        self.root = root
        self.employee = employee
        self.items = checkout_items
        self.root.configure(bg=BG)

        # Main container (TOP)
        main = tk.Frame(root, bg=BG)
        main.pack(pady=5)

        # Header
        build_header(main)

        # Title
        tk.Label(main,
                 text="EQUIPMENT CHECKOUT RECEIPT",
                 font=("Arial", 20, "bold"),
                 bg=BG, fg=FG).pack(pady=5)

        # ============================================================
        # EMPLOYEE + SUPERVISOR INFO (2 COLUMNS)
        # ============================================================
        info = tk.Frame(main, bg=BG)
        info.pack(fill="x", pady=5)

        left = tk.Frame(info, bg=BG)
        right = tk.Frame(info, bg=BG)

        left.pack(side="left", expand=True, fill="both", padx=10)
        right.pack(side="left", expand=True, fill="both", padx=10)

        # Section titles
        tk.Label(left, text="Employee Information",
                 font=("Arial", 14, "bold"), bg=BG).pack(anchor="w")
        tk.Label(right, text="Supervisor Information",
                 font=("Arial", 14, "bold"), bg=BG).pack(anchor="w")

        # Helper row function
        def row(parent, label, value):
            r = tk.Frame(parent, bg=BG)
            r.pack(anchor="w")
            tk.Label(r, text=f"{label}: ",
                     font=("Arial", 12, "bold"), bg=BG).pack(side="left")
            tk.Label(r, text=value,
                     font=("Arial", 12), bg=BG).pack(side="left")

        # LEFT COLUMN — EMPLOYEE INFO
        row(left, "Name", f"{employee['first_name']} {employee['last_name']}")
        row(left, "Employee ID", employee["employee_id"])
        row(left, "Department", employee["department"])
        row(left, "Phone", employee["phone"])
        row(left, "Email", employee["email"])

        # RIGHT COLUMN — SUPERVISOR INFO
        row(right, "Supervisor", employee["supervisor_name"])
        row(right, "Sup. Phone", employee["supervisor_phone"])
        row(right, "Sup. Email", employee["supervisor_email"])

        # ============================================================
        # EQUIPMENT TABLE
        # ============================================================
        table_frame = tk.Frame(main, bg=BG)
        table_frame.pack(pady=5)

        tk.Label(table_frame, text="Equipment Borrowed",
                 font=("Arial", 14, "bold"), bg=BG).pack(anchor="w")

        tree = ttk.Treeview(table_frame,
                            columns=("id", "name", "qty", "notes"),
                            show="headings",
                            height=5)
        tree.heading("id", text="ID")
        tree.heading("name", text="Description")
        tree.heading("qty", text="Qty")
        tree.heading("notes", text="Notes")

        tree.column("id", width=70, anchor="center")
        tree.column("name", width=200, anchor="w")
        tree.column("qty", width=50, anchor="center")
        tree.column("notes", width=200, anchor="w")

        tree.pack()

        for item in checkout_items:
            tree.insert("", "end",
                        values=(item["id"], item["name"], item["qty"], item["notes"]))

        # ============================================================
        # PICKUP / RETURN DATES
        # ============================================================
        dates_frame = tk.Frame(main, bg=BG)
        dates_frame.pack(pady=5, anchor="w")

        pickup = checkout_items[0]["pickup"] if checkout_items else ""
        ret = checkout_items[0]["return"] if checkout_items else ""

        row(dates_frame, "Pickup Date", pickup)
        row(dates_frame, "Return Date", ret)
        row(dates_frame, "Total Items", str(sum(i["qty"] for i in checkout_items)))

        # ============================================================
        # ACKNOWLEDGMENT (COMPACT VERSION)
        # ============================================================
        ack_frame = tk.Frame(main, bg=BG)
        ack_frame.pack(pady=5, fill="x")

        tk.Label(ack_frame, text="Borrower Acknowledgment",
                 font=("Arial", 14, "bold"), bg=BG).pack(anchor="w")

        ack_text = (
            "• Equipment is borrowed in good condition.\n"
            "• Employee is responsible for proper use and timely return.\n"
            "• Items must be returned clean and undamaged.\n"
            "• Loss or damage may result in liability.\n"
            "• Items must be returned by the assigned date.\n"
            "• Report any issues to the Depot Clerk immediately."
        )

        tk.Label(ack_frame, text=ack_text,
                 font=("Arial", 12), bg=BG, justify="left").pack(anchor="w")

        # ============================================================
        # SIGNATURE BLOCKS
        # ============================================================
        sig_frame = tk.Frame(main, bg=BG)
        sig_frame.pack(pady=5, fill="x")

        tk.Label(sig_frame,
                 text="Employee Signature: ____________________    Date: ________",
                 font=("Arial", 12), bg=BG).pack(anchor="w", pady=2)

        tk.Label(sig_frame,
                 text="Clerk Signature:    ____________________    Date: ________",
                 font=("Arial", 12), bg=BG).pack(anchor="w", pady=2)

        # ============================================================
        # BUTTONS
        # ============================================================
        btn_frame = tk.Frame(main, bg=BG)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Cancel",
                  font=("Arial", 14), width=10,
                  bg=BTN_BG, command=self.cancel).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Save & Print",
                  font=("Arial", 14), width=12,
                  bg=BTN_BG, command=self.save_and_print).pack(side="right", padx=10)

    # ============================================================
    # SAVE & PRINT
    # ============================================================
    def save_and_print(self):
        save_path = os.path.join(os.path.dirname(__file__), "data", "checkout_receipts")
        os.makedirs(save_path, exist_ok=True)

        filename = f"receipt_{self.employee['employee_id']}.txt"
        full_path = os.path.join(save_path, filename)

        with open(full_path, "w") as f:
            f.write("GB MANUFACTURING - EQUIPMENT CHECKOUT RECEIPT\n")
            f.write("------------------------------------------------------------\n\n")
            f.write(f"Employee: {self.employee['first_name']} {self.employee['last_name']}\n")
            f.write(f"Employee ID: {self.employee['employee_id']}\n")
            f.write(f"Department: {self.employee['department']}\n")
            f.write(f"Supervisor: {self.employee['supervisor_name']}\n\n")

            f.write("Equipment Borrowed:\n")
            for item in self.items:
                f.write(f"- {item['id']} | {item['name']} | Qty: {item['qty']} | Notes: {item['notes']}\n")

            f.write("\nAcknowledgment:\n")
            f.write("Employee agrees to return equipment on time and in good condition.\n")

        os.startfile(full_path, "print")
        messagebox.showinfo("Saved", "Receipt saved and sent to printer.")

    # ============================================================
    # CANCEL
    # ============================================================
    def cancel(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        DepotMenu(self.root)


class ReturnReceiptWindow:
    def __init__(self, root, employee, returned_items, remaining_items, return_date, notes):
        self.root = root
        self.employee = employee
        self.returned_items = returned_items
        self.remaining_items = remaining_items
        self.return_date = return_date
        self.notes = notes

        self.root.configure(bg=BG)

        main = tk.Frame(root, bg=BG)
        main.place(relx=0.5, rely=0.03, anchor="n")

        build_header(main)

        tk.Label(main,
                 text="EQUIPMENT RETURN RECEIPT",
                 font=("Arial", 26, "bold"),
                 bg=BG, fg=FG).pack(pady=10)

        # ---------------- EMPLOYEE INFO ----------------
        info = tk.Frame(main, bg=BG)
        info.pack(pady=5, fill="x")

        tk.Label(info, text="Employee Information",
                 font=("Arial", 18, "bold"),
                 bg=BG, fg=FG).pack(anchor="w", pady=(0, 5))

        def row(parent, label, value):
            r = tk.Frame(parent, bg=BG)
            r.pack(anchor="w")
            tk.Label(r, text=f"{label}: ",
                     font=("Arial", 14, "bold"),
                     bg=BG, fg=FG).pack(side="left")
            tk.Label(r, text=value,
                     font=("Arial", 14),
                     bg=BG, fg=FG).pack(side="left")

        full_name = f"{employee['first_name']} {employee['last_name']}"
        row(info, "Name", full_name)
        row(info, "Employee ID", employee["employee_id"])
        if "department" in employee:
            row(info, "Department", employee["department"])
        row(info, "Return Date", return_date)

        if notes:
            row(info, "Overall Notes", notes)

        # ---------------- ITEMS RETURNED ----------------
        tk.Label(main, text="Items Returned",
                 font=("Arial", 18, "bold"),
                 bg=BG, fg=FG).pack(anchor="w", padx=10, pady=(15, 5))

        returned_frame = tk.Frame(main, bg=BG)
        returned_frame.pack(fill="x")

        self.returned_tree = ttk.Treeview(
            returned_frame,
            columns=("id", "name", "qty", "condition"),
            show="headings",
            height=6
        )
        self.returned_tree.heading("id", text="ID")
        self.returned_tree.heading("name", text="Description")
        self.returned_tree.heading("qty", text="Qty Returned")
        self.returned_tree.heading("condition", text="Condition")

        self.returned_tree.column("id", width=80, anchor="center")
        self.returned_tree.column("name", width=220, anchor="w")
        self.returned_tree.column("qty", width=110, anchor="center")
        self.returned_tree.column("condition", width=110, anchor="center")

        self.returned_tree.pack(fill="x")

        for item in self.returned_items:
            # (id, name, qty_returned, condition)
            self.returned_tree.insert("", "end", values=item)

        # ---------------- ITEMS STILL CHECKED OUT ----------------
        if self.remaining_items:
            tk.Label(main, text="Items Still Checked Out",
                     font=("Arial", 18, "bold"),
                     bg=BG, fg=FG).pack(anchor="w", padx=10, pady=(15, 5))

            remaining_frame = tk.Frame(main, bg=BG)
            remaining_frame.pack(fill="x")

            self.remaining_tree = ttk.Treeview(
                remaining_frame,
                columns=("id", "name", "qty", "due"),
                show="headings",
                height=5
            )
            self.remaining_tree.heading("id", text="ID")
            self.remaining_tree.heading("name", text="Description")
            self.remaining_tree.heading("qty", text="Qty Remaining")
            self.remaining_tree.heading("due", text="Due Date")

            self.remaining_tree.column("id", width=80, anchor="center")
            self.remaining_tree.column("name", width=240, anchor="w")
            self.remaining_tree.column("qty", width=120, anchor="center")
            self.remaining_tree.column("due", width=120, anchor="center")

            self.remaining_tree.pack(fill="x")

            for item in self.remaining_items:
                # (id, name, qty_remaining, due_date)
                self.remaining_tree.insert("", "end", values=item)

        # ---------------- SIGNATURE + BUTTONS ----------------
        sig = tk.Frame(main, bg=BG)
        sig.pack(pady=20, fill="x")

        tk.Label(sig, text="Clerk Signature: ________________________________",
                 font=("Arial", 14), bg=BG, fg=FG).pack(anchor="w", padx=10)

        tk.Label(sig, text="Employee Acknowledgment: ________________________",
                 font=("Arial", 14), bg=BG, fg=FG).pack(anchor="w", padx=10, pady=5)

        bottom = tk.Frame(main, bg=BG)
        bottom.pack(pady=20, fill="x")

        tk.Button(bottom, text="Back",
                  font=("Arial", 16), width=12,
                  bg=BTN_BG, fg=FG,
                  command=self.back).pack(side="left", padx=10)

        tk.Button(bottom, text="Cancel",
                  font=("Arial", 16), width=12,
                  bg=BTN_BG, fg=FG,
                  command=self.cancel).pack(side="left", padx=10)

        tk.Button(bottom, text="Save & Print",
                  font=("Arial", 16), width=15,
                  bg=BTN_BG, fg=FG,
                  command=self.save_and_print).pack(side="right", padx=10)

    def back(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        ReturnWindow(self.root, self.employee)

    def cancel(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        DepotMenu(self.root)

    def save_and_print(self):
        # Placeholder for real save/print
        messagebox.showinfo("Saved", "Return receipt has been saved and sent to printer.")
        for widget in self.root.winfo_children():
            widget.destroy()
        DepotMenu(self.root)




# ---------------------------------------------------------
# RUN DIRECTLY FOR TESTING
# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    DepotMenu(root)
    root.mainloop()
