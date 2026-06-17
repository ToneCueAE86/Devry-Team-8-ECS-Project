import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

BG = "#e6e6e6"
BTN_BG = "#c0c0c0"
FG = "black"

from datetime import datetime

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


class EmployeeProfileWindow(tk.Frame):
    def __init__(self, root, employee, mode="checkout"):
        super().__init__(root, bg=BG)
        self.root = root
        self.employee = employee
        self.mode = mode

        for widget in self.root.winfo_children():
            widget.destroy()

        self.pack(fill="both", expand=True)

        # ---------------- HEADER ----------------
        build_header(self)

        tk.Label(self,
                 text="EMPLOYEE PROFILE",
                 font=("Arial", 28, "bold"),
                 bg=BG, fg=FG).pack(pady=10)

        # ---------------- PHOTO PLACEHOLDER ----------------
        photo_frame = tk.Frame(self, bg=BG)
        photo_frame.pack(pady=10)

        canvas = tk.Canvas(photo_frame, width=150, height=180,
                           bg="white", highlightbackground="black")
        canvas.pack()
        canvas.create_rectangle(5, 5, 145, 175, outline="black", width=2)
        canvas.create_text(75, 90, text="PHOTO", font=("Arial", 14, "bold"))

        # ---------------- TWO COLUMN LAYOUT ----------------
        info_frame = tk.Frame(self, bg=BG)
        info_frame.pack(pady=10)

        left = tk.Frame(info_frame, bg=BG)
        right = tk.Frame(info_frame, bg=BG)
        left.grid(row=0, column=0, padx=40, sticky="n")
        right.grid(row=0, column=1, padx=40, sticky="n")

        def row(parent, label, value):
            r = tk.Frame(parent, bg=BG)
            r.pack(anchor="w", pady=2)
            tk.Label(r, text=f"{label}: ",
                     font=("Arial", 14, "bold"),
                     bg=BG).pack(side="left")
            tk.Label(r, text=value,
                     font=("Arial", 14),
                     bg=BG).pack(side="left")

        # LEFT COLUMN — EMPLOYEE INFO
        full_name = f"{employee['first_name']} {employee['last_name']}"
        row(left, "Name", full_name)
        row(left, "Employee ID", employee["employee_id"])
        row(left, "Department", employee["work_location"])
        row(left, "Status", employee["status"])
        row(left, "Phone", employee["phone"])
        row(left, "Email", employee["email"])

        # RIGHT COLUMN — SUPERVISOR INFO
        row(right, "Supervisor", employee["supervisor_name"])
        row(right, "Sup. Phone", employee["supervisor_phone"])
        row(right, "Sup. Email", employee["supervisor_email"])

        # ---------------- CERTIFICATIONS ----------------
        cert_frame = tk.Frame(self, bg=BG)
        cert_frame.pack(pady=20)

        tk.Label(cert_frame,
                 text="Certifications / Authorized Equipment",
                 font=("Arial", 18, "bold"),
                 bg=BG, fg=FG).pack(anchor="w")

        cert_list = employee.get("certifications", ["None Listed"])

        for cert in cert_list:
            tk.Label(cert_frame,
                     text=f"• {cert}",
                     font=("Arial", 14),
                     bg=BG, fg=FG).pack(anchor="w")

        # ---------------- BUTTONS ----------------
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=30)

        tk.Button(btn_frame,
                  text="Back",
                  font=("Arial", 16),
                  width=12,
                  bg=BTN_BG,
                  command=self.go_back).grid(row=0, column=0, padx=20)

        if self.mode == "checkout":
            tk.Button(btn_frame,
                      text="Proceed to Checkout",
                      font=("Arial", 16),
                      width=20,
                      bg=BTN_BG,
                      command=self.go_checkout).grid(row=0, column=1, padx=20)
        else:
            tk.Button(btn_frame,
                      text="Proceed to Return",
                      font=("Arial", 16),
                      width=20,
                      bg=BTN_BG,
                      command=self.go_return).grid(row=0, column=1, padx=20)

    def go_back(self):
        from depot import EmployeeVerificationWindow
        for widget in self.root.winfo_children():
            widget.destroy()
        EmployeeVerificationWindow(self.root)

    def go_checkout(self):
        from depot import CheckoutFormWindow
        for widget in self.root.winfo_children():
            widget.destroy()
        CheckoutFormWindow(self.root, self.employee)

    def go_return(self):
        from depot import ReturnWindow
        for widget in self.root.winfo_children():
            widget.destroy()
        ReturnWindow(self.root, self.employee)
