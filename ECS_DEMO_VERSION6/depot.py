import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from tkcalendar import Calendar
import datetime

class DepotMenu:
    def __init__(self, username):
        self.username = username

        """
        self.window = tk.Tk()
        self.window.title("Depot Department")
        #self.window.geometry("600x500")
        self.window.state("zoomed")
        self.window.configure(bg="#1e1e1e")
        self.build_header(self.window)

        # your existing depot UI here...
        tk.Button(
            self.window,
            text="Process Equipment Checkout",
            font=("Arial", 16),
            width=30,
            command=self.open_process_checkout
        ).pack(pady=40)"""

    def build_header(self, parent):
        from datetime import datetime

        header = tk.Frame(parent, bg="#1e1e1e")
        header.pack(fill="x", pady=10)

        # ----- CIRCLE LOGO -----
        canvas = tk.Canvas(header, width=180, height=180,
                           bg="#1e1e1e", highlightthickness=0)
        canvas.pack()

        # Circle outline
        canvas.create_oval(10, 10, 170, 170, outline="white", width=4)

        # Text inside circle
        canvas.create_text(90, 70, text="GB",
                           fill="white", font=("Arial", 32, "bold"))
        canvas.create_text(90, 115, text="MANUFACTURING",
                           fill="white", font=("Arial", 12, "bold"))

        # ----- DATE & TIME -----
        now = datetime.now().strftime("%A, %B %d, %Y | %I:%M %p")
        tk.Label(
            header,
            text=now,
            font=("Arial", 12),
            fg="white",
            bg="#1e1e1e"
        ).pack(pady=5)

        # ----- DEPOT DEPARTMENT -----
        tk.Label(
            header,
            text="Depot Department",
            font=("Arial", 14, "bold"),
            fg="#3a7bd5",
            bg="#1e1e1e"
        ).pack(pady=(5, 0))



    def open_process_checkout(self):
        # SMALL POP-UP WINDOW (TOP-LEFT CORNER)
        win = tk.Toplevel(self.window)
        self.window.state("zoomed")
       # win.geometry("500x350+0+0")   # <-- small window, top-left corner
        win.configure(bg="#1e1e1e")

        # HEADER
        self.build_header(win)

        # MAIN FRAME
        frame = tk.Frame(win, bg="#1e1e1e")
        frame.pack(pady=30)

        # LABEL
        tk.Label(
            frame,
            text="Enter Employee ID:",
            font=("Arial", 16),
            fg="white",
            bg="#1e1e1e"
        ).pack(pady=10)

        # ENTRY BOX
        emp_id_entry = tk.Entry(frame, font=("Arial", 16), width=20)
        emp_id_entry.pack(pady=10)

        # BUTTON ROW
        btn_row = tk.Frame(frame, bg="#1e1e1e")
        btn_row.pack(pady=20)

        # VERIFY BUTTON
        tk.Button(
            btn_row,
            text="Verify",
            font=("Arial", 14),
            bg="#3a7bd5",
            fg="white",
            width=9,
            command=lambda: self.verify_employee_id(emp_id_entry.get(), win)
        ).grid(row=0, column=0, padx=10)

        # CANCEL BUTTON
        tk.Button(
            btn_row,
            text="Cancel",
            font=("Arial", 14),
            bg="gray",
            fg="white",
            width=9,
            command=win.destroy
        ).grid(row=0, column=1, padx=10)

    def verify_employee_id(self, emp_id, window):
        emp_id = emp_id.strip().upper()

        try:
            with open("borrower_registry.json", "r") as f:
                borrowers = json.load(f)
        except:
            messagebox.showerror("Error", "Could not load borrower_registry.json")
            return

        match = next(
            (emp for emp in borrowers if emp.get("employee_id", "").upper() == emp_id),
            None
        )

        if match:
            window.destroy()
            self.open_employee_profile_window(match)
        else:
            messagebox.showerror("Not Found", f"Employee ID '{emp_id}' not found.")

    def open_employee_profile_window(self, employee):
        """
        ISOLATED AA-STYLE METHOD (NO SCROLL VERSION)
        Clean, centered, self-contained. Easy to debug or replace.
        """

        # ---------------- WINDOW SETUP ----------------
        win = tk.Toplevel(self.window)
        win.title("Employee Profile")
        win.configure(bg="#1e1e1e")

        # Center window
        width, height = 700,1100
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

        # Header
        self.build_header(win)

        # ---------------- MAIN CONTENT AREA (NO SCROLL) ----------------
        inner = tk.Frame(win, bg="#1e1e1e")
        inner.pack(fill="both", expand=True, padx=40, pady=20)

        # ---------------- BASIC INFO ----------------
        section_basic = tk.LabelFrame(
            inner, text="Employee Information",
            font=("Arial", 12, "bold"),
            fg="white", bg="#1e1e1e",
            bd=2, relief="groove", labelanchor="n"
        )
        section_basic.pack(fill="x", pady=10)

        grid = tk.Frame(section_basic, bg="#1e1e1e")
        grid.pack(padx=10, pady=10)

        def add_row(r, label, value):
            tk.Label(grid, text=f"{label}:", fg="white", bg="#1e1e1e",
                     font=("Arial", 11, "bold")).grid(row=r, column=0, sticky="e", padx=5, pady=3)
            tk.Label(grid, text=value, fg="white", bg="#1e1e1e",
                     font=("Arial", 11), wraplength=400, justify="left").grid(row=r, column=1, sticky="w", padx=5,
                                                                              pady=3)

        r = 0
        add_row(r, "First Name", employee.get("first_name", ""));
        r += 1
        add_row(r, "Last Name", employee.get("last_name", ""));
        r += 1
        add_row(r, "Employee ID", employee.get("employee_id", ""));
        r += 1
        add_row(r, "Job Title", employee.get("job_title", ""));
        r += 1
        add_row(r, "Department", employee.get("department", ""));
        r += 1
        add_row(r, "Status", employee.get("status", ""));
        r += 1
        add_row(r, "Phone", employee.get("phone", ""));
        r += 1
        add_row(r, "Email", employee.get("email", ""));
        r += 1
        add_row(r, "Work Location", employee.get("work_location", ""));
        r += 1
        add_row(r, "Notes", employee.get("notes", ""));
        r += 1

        # ---------------- SPECIALIZATIONS ----------------
        section_spec = tk.LabelFrame(
            inner, text="Specializations",
            font=("Arial", 12, "bold"),
            fg="white", bg="#1e1e1e",
            bd=2, relief="groove", labelanchor="n"
        )
        section_spec.pack(fill="x", pady=10)

        spec_frame = tk.Frame(section_spec, bg="#1e1e1e")
        spec_frame.pack(padx=10, pady=10, anchor="w")

        specs = employee.get("specializations", [])
        if specs:
            for spec in specs:
                tk.Label(spec_frame, text=f"• {spec}", fg="white",
                         bg="#1e1e1e", font=("Arial", 11)).pack(anchor="w")
        else:
            tk.Label(spec_frame, text="No specializations on file",
                     fg="white", bg="#1e1e1e", font=("Arial", 11, "italic")).pack(anchor="w")

        # ---------------- CERTIFICATIONS ----------------
        section_cert = tk.LabelFrame(
            inner, text="Certifications",
            font=("Arial", 12, "bold"),
            fg="white", bg="#1e1e1e",
            bd=2, relief="groove", labelanchor="n"
        )
        section_cert.pack(fill="x", pady=10)

        cert_frame = tk.Frame(section_cert, bg="#1e1e1e")
        cert_frame.pack(padx=10, pady=10, anchor="w")

        certs = employee.get("certifications", [])
        if certs:
            for cert in certs:
                tk.Label(cert_frame,
                         text=f"- {cert.get('name', '')} (Issued: {cert.get('issued', '')})",
                         fg="white", bg="#1e1e1e", font=("Arial", 11)).pack(anchor="w")
        else:
            tk.Label(cert_frame, text="No certifications on file",
                     fg="white", bg="#1e1e1e", font=("Arial", 11, "italic")).pack(anchor="w")

        # ---------------- SUPERVISOR INFO ----------------
        section_sup = tk.LabelFrame(
            inner, text="Supervisor Information",
            font=("Arial", 12, "bold"),
            fg="white", bg="#1e1e1e",
            bd=2, relief="groove", labelanchor="n"
        )
        section_sup.pack(fill="x", pady=10)

        sup_grid = tk.Frame(section_sup, bg="#1e1e1e")
        sup_grid.pack(padx=10, pady=10)

        def add_sup(label, value):
            tk.Label(sup_grid, text=f"{label}:", fg="white", bg="#1e1e1e",
                     font=("Arial", 11, "bold")).pack(anchor="w")
            tk.Label(sup_grid, text=value, fg="white", bg="#1e1e1e",
                     font=("Arial", 11), wraplength=400, justify="left").pack(anchor="w", pady=(0, 5))

        add_sup("Supervisor Name", employee.get("supervisor_name", ""))
        add_sup("Supervisor Phone", employee.get("supervisor_contact", {}).get("phone", ""))
        add_sup("Supervisor Email", employee.get("supervisor_contact", {}).get("email", ""))

        # ---------------- BUTTONS ----------------
        btn_frame = tk.Frame(inner, bg="#1e1e1e")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Cancel", font=("Arial", 14),
                  width=12, bg="#5a5a5a", fg="white",
                  command=win.destroy).grid(row=0, column=0, padx=20)

        tk.Button(btn_frame, text="Next", font=("Arial", 14),
                  width=12, bg="#3a7bd5", fg="white",
                  command=lambda: [win.destroy(), self.open_equipment_checkout_window(employee)
]
                  ).grid(row=0, column=1, padx=20)

    def open_equipment_checkout_window(self, employee):

        # ---------------- WINDOW SETUP ----------------
        win = tk.Toplevel(self.window)
        win.title("Equipment Checkout")
        win.configure(bg="#1e1e1e")
        win.state("zoomed")

        # ---------------- MAIN LAYOUT ----------------
        # Top = scrollable content
        # Bottom = fixed buttons
        main = tk.Frame(win, bg="#1e1e1e")
        main.pack(fill="both", expand=True)

        # ---------------- SCROLLABLE TOP AREA ----------------
        top_frame = tk.Frame(main, bg="#1e1e1e")
        top_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(top_frame, bg="#1e1e1e", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(top_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        inner = tk.Frame(canvas, bg="#1e1e1e")
        canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner.bind("<Configure>", on_configure)

        # ---------------- HEADER ----------------
        self.build_header(inner)

        # ---------------- CONTENT ----------------
        content = tk.Frame(inner, bg="#1e1e1e")
        content.pack(fill="both", expand=True, padx=40, pady=20)

        # ---------------- BORROWER INFO ----------------
        section_borrower = tk.LabelFrame(
            content, text="Borrower Information",
            font=("Arial", 12, "bold"),
            fg="white", bg="#1e1e1e",
            bd=2, relief="groove", labelanchor="n"
        )
        section_borrower.pack(fill="x", pady=10)

        tk.Label(section_borrower,
                 text=f"Borrower: {employee.get('first_name', '')} {employee.get('last_name', '')} ({employee.get('employee_id', '')})",
                 fg="white", bg="#1e1e1e", font=("Arial", 11)).pack(anchor="w", padx=10, pady=2)

        tk.Label(section_borrower,
                 text=f"Department: {employee.get('department', '')}",
                 fg="white", bg="#1e1e1e", font=("Arial", 11)).pack(anchor="w", padx=10, pady=2)

        tk.Label(section_borrower,
                 text=f"Status: {employee.get('status', '')}",
                 fg="white", bg="#1e1e1e", font=("Arial", 11)).pack(anchor="w", padx=10, pady=2)

        # ---------------- LOAD EQUIPMENT DB ----------------
        try:
            with open("equipment_db.json", "r") as f:
                equipment_list = json.load(f)
        except:
            equipment_list = []

        # ---------------- SEARCH EQUIPMENT ----------------
        section_search = tk.LabelFrame(
            content, text="Search Equipment",
            font=("Arial", 12, "bold"),
            fg="white", bg="#1e1e1e",
            bd=2, relief="groove", labelanchor="n"
        )
        section_search.pack(fill="x", pady=10)

        tk.Label(section_search, text="Type equipment name or ID:",
                 fg="white", bg="#1e1e1e", font=("Arial", 11)).pack(anchor="w", padx=10, pady=5)

        search_var = tk.StringVar()
        tk.Entry(section_search, textvariable=search_var, font=("Arial", 12), width=40).pack(padx=10, pady=5)

        listbox = tk.Listbox(section_search, font=("Arial", 11), width=50, height=6)
        listbox.pack(padx=10, pady=10)

        def update_listbox(*args):
            listbox.delete(0, tk.END)
            text = search_var.get().lower()
            for eq in equipment_list:
                if text in eq.get("name", "").lower() or text in eq.get("id", "").lower():
                    listbox.insert(tk.END, f"{eq['name']} ({eq['id']})")

        search_var.trace("w", update_listbox)
        update_listbox()

        # ---------------- CHECKOUT LIST ----------------
        section_checkout = tk.LabelFrame(
            content, text="Checkout List",
            font=("Arial", 12, "bold"),
            fg="white", bg="#1e1e1e",
            bd=2, relief="groove", labelanchor="n"
        )
        section_checkout.pack(fill="x", pady=10)

        checkout_items = []
        checkout_frame = tk.Frame(section_checkout, bg="#1e1e1e")
        checkout_frame.pack(fill="x", padx=10, pady=10)

        def refresh_checkout():
            for widget in checkout_frame.winfo_children():
                widget.destroy()

            headers = ["Equipment ID", "Name", "Qty", "+", "-", "Remove"]
            for i, h in enumerate(headers):
                tk.Label(checkout_frame, text=h, fg="white", bg="#1e1e1e",
                         font=("Arial", 11, "bold")).grid(row=0, column=i, padx=5, pady=5)

            for r, item in enumerate(checkout_items, start=1):
                tk.Label(checkout_frame, text=item["equipment_id"], fg="white", bg="#1e1e1e").grid(row=r, column=0)
                tk.Label(checkout_frame, text=item["equipment_name"], fg="white", bg="#1e1e1e").grid(row=r, column=1)
                tk.Label(checkout_frame, text=item["quantity"], fg="white", bg="#1e1e1e").grid(row=r, column=2)

                tk.Button(checkout_frame, text="+", command=lambda i=item: increase_qty(i)).grid(row=r, column=3)
                tk.Button(checkout_frame, text="-", command=lambda i=item: decrease_qty(i)).grid(row=r, column=4)
                tk.Button(checkout_frame, text="X", command=lambda i=item: remove_item(i)).grid(row=r, column=5)

        def increase_qty(item):
            item["quantity"] += 1
            refresh_checkout()

        def decrease_qty(item):
            if item["quantity"] > 1:
                item["quantity"] -= 1
            refresh_checkout()

        def remove_item(item):
            checkout_items.remove(item)
            refresh_checkout()

        # ---------------- ADD ITEM ----------------
        def add_selected_item(event):
            selection = listbox.get(tk.ACTIVE)
            if not selection:
                return

            name, eid = selection.rsplit("(", 1)
            eid = eid.replace(")", "")

            eq = next((e for e in equipment_list if e["id"] == eid), None)
            if not eq:
                return

            if eq.get("status") != "Operational":
                messagebox.showwarning("Unavailable",
                                       f"{eq['name']} cannot be checked out.\nStatus: {eq['status']}")
                return

            borrower_certs = [c.get("name", "") for c in employee.get("certifications", [])]
            required_cert = eq.get("certification_required", "")

            if required_cert != "None" and required_cert not in borrower_certs:
                messagebox.showwarning("Not Authorized",
                                       f"{employee['first_name']} is NOT certified for {eq['name']}.\n"
                                       f"Required: {required_cert}")
                return

            checkout_items.append({
                "equipment_id": eid,
                "equipment_name": eq["name"],
                "quantity": 1
            })
            refresh_checkout()

        listbox.bind("<<ListboxSelect>>", add_selected_item)

        # ---------------- PICKUP & RETURN DATES ----------------
        section_dates = tk.LabelFrame(
            content, text="Pickup & Return Dates",
            font=("Arial", 12, "bold"),
            fg="white", bg="#1e1e1e",
            bd=2, relief="groove", labelanchor="n"
        )
        section_dates.pack(fill="x", pady=10)

        tk.Label(section_dates, text="Pickup Date:", fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=10, pady=5)
        pickup_var = tk.StringVar(value=str(datetime.date.today()))
        tk.Entry(section_dates, textvariable=pickup_var, width=15).grid(row=0, column=1, padx=5)

        tk.Label(section_dates, text="Return Date:", fg="white", bg="#1e1e1e").grid(row=1, column=0, padx=10, pady=5)
        return_var = tk.StringVar(value=str(datetime.date.today() + datetime.timedelta(days=7)))
        tk.Entry(section_dates, textvariable=return_var, width=15).grid(row=1, column=1, padx=5)

        # ---------------- FIXED BOTTOM BUTTONS (STICKY FOOTER) ----------------
        footer = tk.Frame(main, bg="#1e1e1e")
        footer.pack(fill="x", pady=20)

        tk.Button(footer, text="Cancel", font=("Arial", 14),
                  width=12, bg="#5a5a5a", fg="white",
                  command=lambda: [win.destroy(), self.open_depot_menu()]
                  ).pack(side="right", padx=20)

        tk.Button(footer, text="Proceed", font=("Arial", 14),
                  width=12, bg="#3a7bd5", fg="white",
                  command=lambda: self.open_final_confirmation_window(
                      {
                          "name": f"{employee.get('first_name', '')} {employee.get('last_name', '')}",
                          "id": employee.get('employee_id', ''),
                          "department": employee.get('department', ''),
                          "status": employee.get('status', '')
                      },
                      checkout_items,
                      pickup_var.get(),
                      return_var.get()
                  )
                  ).pack(side="right", padx=20)

    def open_final_confirmation_window(self, employee, checkout_items, pickup_date, return_date):
        print("DEBUG EMPLOYEE:", employee)

        import os
        import tkinter as tk

        # ---------------- WINDOW SETUP ----------------
        win = tk.Toplevel(self.window)
        win.title("Equipment Checkout Confirmation")
        win.configure(bg="#1e1e1e")

        # Centered fixed-size window
        WIDTH, HEIGHT = 800, 900
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (WIDTH // 2)
        y = (win.winfo_screenheight() // 2) - (HEIGHT // 2)
        win.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

        # ---------------- MAIN CENTERED CONTAINER ----------------
        container = tk.Frame(win, bg="#1e1e1e")
        container.pack(expand=True)

        box = tk.Frame(container, bg="#2b2b2b", bd=3, relief="ridge")
        box.pack(pady=20, padx=20)

        # ---------------- HEADER ----------------
        header = tk.Label(
            box,
            text="GB MANUFACTURING\nEQUIPMENT CHECKOUT CONFIRMATION",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#2b2b2b",
            pady=20
        )
        header.pack(fill="x")

        # ---------------- EMPLOYEE INFO ----------------
        frame_emp = tk.LabelFrame(
            box,
            text="Employee Information",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#2b2b2b"
        )
        frame_emp.pack(fill="x", padx=20, pady=10)

        tk.Label(
            frame_emp,
            text=f"Name: {employee.get('name', 'N/A')} ({employee.get('id', 'N/A')})",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10, pady=3)

        tk.Label(
            frame_emp,
            text=f"Department: {employee.get('department', 'N/A')}",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10, pady=3)

        tk.Label(
            frame_emp,
            text=f"Status: {employee.get('status', 'N/A')}",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10, pady=3)

        # ---------------- EQUIPMENT LIST ----------------
        frame_eq = tk.LabelFrame(
            box,
            text="Equipment Borrowed",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#2b2b2b"
        )
        frame_eq.pack(fill="x", padx=20, pady=10)

        for item in checkout_items:
            tk.Label(
                frame_eq,
                text=f"{item['equipment_id']}   {item['equipment_name']}   Qty: {item['quantity']}   Condition: Good",
                fg="white",
                bg="#2b2b2b",
                font=("Arial", 12)
            ).pack(anchor="w", padx=10, pady=3)

        tk.Label(
            frame_eq,
            text=f"Total Items: {sum(i['quantity'] for i in checkout_items)}",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)

        # ---------------- DATES ----------------
        frame_dates = tk.LabelFrame(
            box,
            text="Pickup & Return Dates",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#2b2b2b"
        )
        frame_dates.pack(fill="x", padx=20, pady=10)

        tk.Label(
            frame_dates,
            text=f"Pickup Date: {pickup_date}",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10, pady=3)

        tk.Label(
            frame_dates,
            text=f"Return Date: {return_date}",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10, pady=3)

        # ---------------- ACKNOWLEDGMENT ----------------
        frame_ack = tk.LabelFrame(
            box,
            text="Borrower Acknowledgment",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#2b2b2b"
        )
        frame_ack.pack(fill="x", padx=20, pady=10)

        ack_text = (
            "• All equipment is borrowed in good working condition.\n"
            "• Employee is responsible for proper use and timely return.\n"
            "• Loss, damage, or misuse may result in financial liability.\n"
            "• Equipment must be returned clean and functional.\n"
            "• Late returns may result in account suspension.\n"
            "• Missing or damaged items must be reported immediately."
        )

        tk.Label(
            frame_ack,
            text=ack_text,
            justify="left",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10, pady=5)

        # ---------------- SIGNATURES ----------------
        frame_sig = tk.LabelFrame(
            box,
            text="Signatures",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#2b2b2b"
        )
        frame_sig.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_sig, text="Employee Signature: ____________________________", fg="white", bg="#2b2b2b",
                 font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(frame_sig, text="Date: ____________________", fg="white", bg="#2b2b2b",
                 font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

        tk.Label(frame_sig, text="Clerk Signature:    ____________________________", fg="white", bg="#2b2b2b",
                 font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(frame_sig, text="Date: ____________________", fg="white", bg="#2b2b2b",
                 font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

        # ---------------- SAVE & PRINT (SAME LOGIC YOU HAD) ----------------
        def save_and_print():
            form_text = f"""
    GB MANUFACTURING
    EQUIPMENT CHECKOUT FORM
    ------------------------------------------------------------
    Employee: {employee.get('name', 'N/A')} ({employee.get('id', 'N/A')})
    Department: {employee.get('department', 'N/A')}
    Status: {employee.get('status', 'N/A')}

    Pickup Date: {pickup_date}
    Return Date: {return_date}

    Equipment Borrowed:
    """
            for item in checkout_items:
                form_text += f"- {item['equipment_id']} {item['equipment_name']} (Qty {item['quantity']})\n"

            form_text += """
    ------------------------------------------------------------
    Borrower Acknowledgment:
    Employee agrees to all listed responsibilities.

    Employee Signature: ____________________________
    Clerk Signature:    ____________________________
    """

            with open("checkout_form.txt", "w") as f:
                f.write(form_text)

            os.startfile("checkout_form.txt", "print")

        # ---------------- BUTTONS (CENTERED UNDER BOX) ----------------
        btn_frame = tk.Frame(container, bg="#1e1e1e")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Cancel", width=15,
                  bg="#5a5a5a", fg="white", font=("Arial", 12),
                  command=win.destroy).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Save & Print", width=15,
                  bg="#3a7bd5", fg="white", font=("Arial", 12),
                  command=save_and_print).pack(side="left", padx=20)

    def open_depot_menu(self):
        self.window = tk.Toplevel()
        win = self.window
        win.title("Depot Department Menu")
        win.state("zoomed")
        win.configure(bg="#1e1e1e")
#
       #win = tk.Toplevel(self.window)
        #win.title("Depot Department Menu")
        #win.state("zoomed")
        #win.configure(bg="#1e1e1e")"""

        # ---------------- HEADER ----------------
        self.build_header(win)

        # ---------------- MAIN MENU AREA ----------------
        frame = tk.Frame(win, bg="#1e1e1e")
        frame.pack(expand=True)

        title = tk.Label(
            frame,
            text="DEPOT DEPARTMENT",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#1e1e1e",
            pady=20
        )
        title.pack()

        # BUTTON STYLE
        def menu_button(text, command=None):
            return tk.Button(
                frame,
                text=text,
                font=("Arial", 16),
                width=35,
                height=2,
                bg="#3a3a3a",
                fg="white",
                bd=2,
                relief="raised",
                command=command
            )

        # ---------------- BUTTONS ----------------

        # ✔ THIS ONE WORKS — uses your existing checkout method

        #Remove
        menu_button(
            "Process Equipment Checkout",
            command=self.open_process_checkout
        ).pack(pady=10)

        # The rest are placeholders for now
        menu_button("Process Equipment Return",
                    command=lambda: self.placeholder_window("Process Equipment Return")
                    ).pack(pady=10)

        menu_button("Update Equipment Availability",
                    command=lambda: self.placeholder_window("Update Equipment Availability")
                    ).pack(pady=10)

        menu_button("Mark Equipment Lost / Damaged",
                    command=lambda: self.placeholder_window("Mark Equipment Lost / Damaged")
                    ).pack(pady=10)

        menu_button("View All Checked-Out Equipment",
                    command=lambda: self.placeholder_window("View All Checked-Out Equipment")
                    ).pack(pady=10)

        menu_button("View Overdue Equipment",
                    command=lambda: self.placeholder_window("View Overdue Equipment")
                    ).pack(pady=10)

        # ---------------- LOGOUT ----------------
        tk.Button(
            frame,
            text="Logout",
            font=("Arial", 16),
            width=20,
            bg="#5a5a5a",
            fg="white",
            command=lambda: [win.destroy(), self.open_login_window()]
        ).pack(pady=40)

    def placeholder_window(self, title):
        win = tk.Toplevel(self.window)
        win.title(title)
        win.geometry("500x300")
        win.configure(bg="#1e1e1e")

        tk.Label(
            win,
            text=f"{title}\n\n(This feature is under development)",
            font=("Arial", 16),
            fg="white",
            bg="#1e1e1e",
            pady=40
        ).pack()

        tk.Button(
            win,
            text="Close",
            font=("Arial", 14),
            width=12,
            bg="#5a5a5a",
            fg="white",
            command=win.destroy
        ).pack(pady=20)









