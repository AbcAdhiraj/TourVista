import customtkinter as ctk
from tkinter import messagebox, filedialog
from core.management import TravelManagementSystem
from core.exceptions import TourTravelException

# Set appearance
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tour & Travel Management System")
        self.geometry("1100x700")

        # Initialize System
        self.system = TravelManagementSystem()
        self.system.load_data()

        # Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="T&T System", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Sidebar Buttons
        self.btn_customers = self.create_sidebar_button("Customers", 1, self.show_customers)
        self.btn_packages = self.create_sidebar_button("Packages", 2, self.show_packages)
        self.btn_bookings = self.create_sidebar_button("Bookings", 3, self.show_bookings)
        self.btn_hotels = self.create_sidebar_button("Hotels", 4, self.show_hotels)
        self.btn_transports = self.create_sidebar_button("Transports", 5, self.show_transports)
        self.btn_payments = self.create_sidebar_button("Payments", 6, self.show_payments)
        self.btn_schedules = self.create_sidebar_button("Schedules", 7, self.show_schedules)
        self.btn_reports = self.create_sidebar_button("Reports", 8, self.show_reports)
        
        self.btn_save = self.create_sidebar_button("Save Data", 9, self.save_data_action, color="green")
        self.btn_exit = self.create_sidebar_button("Exit", 10, self.quit, color="red")

        # Content Area
        self.content_area = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Start with a Welcome Screen
        self.show_welcome()

    def create_sidebar_button(self, text, row, command, color=None):
        button = ctk.CTkButton(self.sidebar, text=text, command=command)
        if color == "green":
            button.configure(fg_color="#28a745", hover_color="#218838")
        elif color == "red":
            button.configure(fg_color="#dc3545", hover_color="#c82333")
        button.grid(row=row, column=0, padx=20, pady=10, sticky="ew")
        return button

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear_content()
        welcome_label = ctk.CTkLabel(self.content_area, text="Welcome to Tour & Travel Management System", font=ctk.CTkFont(size=24, weight="bold"))
        welcome_label.pack(pady=(100, 20))
        desc_label = ctk.CTkLabel(self.content_area, text="Please select a module from the sidebar to begin.", font=ctk.CTkFont(size=16))
        desc_label.pack(pady=10)

    def save_data_action(self):
        if self.system.save_data():
            messagebox.showinfo("Success", "All data saved successfully!")
        else:
            messagebox.showerror("Error", "Failed to save data.")

    # --- Views ---

    def show_customers(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="Customer Management", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        # Form Frame
        form_frame = ctk.CTkFrame(self.content_area)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Register New Customer", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        entries = {}
        fields = [("Customer ID", "cid"), ("Name", "name"), ("Email", "email"), ("Mobile", "mobile"), ("Address", "address")]
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label).grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=200)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            entries[key] = entry

        def register():
            try:
                self.system.register_customer(
                    entries['cid'].get(), entries['name'].get(), entries['email'].get(),
                    entries['mobile'].get(), entries['address'].get()
                )
                messagebox.showinfo("Success", "Customer registered!")
                self.show_customers() # Refresh
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(form_frame, text="Register", command=register, fg_color="green").grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        # List Frame
        list_frame = ctk.CTkFrame(self.content_area)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(list_frame, text="Registered Customers", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        # Simple List Display
        for cid, customer in self.system.customers.items():
            row_frame = ctk.CTkFrame(list_frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            ctk.CTkLabel(row_frame, text=f"{customer.person_id} | {customer.name} | {customer.email}").pack(side="left", padx=10)
            ctk.CTkButton(row_frame, text="Details", width=60, command=lambda c=customer: self.view_customer_details(c)).pack(side="right", padx=5)

    def view_customer_details(self, customer):
        details = f"ID: {customer.person_id}\n\nName: {customer.name}\n\nEmail: {customer.email}\n\nMobile: {customer.mobile_number}\n\nAddress: {customer.address}"
        messagebox.showinfo("Customer Details", details)

    def show_packages(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="Tour Package Management", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        # Form Frame
        form_frame = ctk.CTkFrame(self.content_area)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Create New Package", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        entries = {}
        fields = [("Package ID", "pid"), ("Package Name", "name"), ("Destination", "dest"), ("Duration", "dur"), ("Price", "price"), ("Hotel ID", "hid"), ("Transport ID", "tid")]
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label).grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=200)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            entries[key] = entry

        def create():
            try:
                self.system.create_package(
                    entries['pid'].get(), entries['name'].get(), entries['dest'].get(),
                    int(entries['dur'].get()), float(entries['price'].get()),
                    hotel_id=entries['hid'].get() if entries['hid'].get() else None,
                    transport_id=entries['tid'].get() if entries['tid'].get() else None
                )
                messagebox.showinfo("Success", "Package created!")
                self.show_packages()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(form_frame, text="Create Package", command=create, fg_color="green").grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        # List Frame
        list_frame = ctk.CTkFrame(self.content_area)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(list_frame, text="Available Packages", font=ctk.CTkFont(weight="bold")).pack(pady=5)

        for pid, pkg in self.system.packages.items():
            row_frame = ctk.CTkFrame(list_frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            ctk.CTkLabel(row_frame, text=f"{pkg.package_id} | {pkg.package_name} ({pkg.destination}) - ${pkg.package_price}").pack(side="left", padx=10)

    def show_bookings(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="Booking Management", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        # Form Frame
        form_frame = ctk.CTkFrame(self.content_area)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Create New Booking", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        entries = {}
        fields = [("Booking ID", "bid"), ("Customer ID", "cid"), ("Package ID", "pid")]
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label).grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=200)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            entries[key] = entry

        def create():
            try:
                self.system.create_booking(entries['bid'].get(), entries['cid'].get(), entries['pid'].get())
                messagebox.showinfo("Success", "Booking created!")
                self.show_bookings()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(form_frame, text="Create Booking", command=create, fg_color="green").grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        # List Frame
        list_frame = ctk.CTkFrame(self.content_area)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(list_frame, text="Current Bookings", font=ctk.CTkFont(weight="bold")).pack(pady=5)

        for bid, b in self.system.bookings.items():
            row_frame = ctk.CTkFrame(list_frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            ctk.CTkLabel(row_frame, text=f"{b.booking_id} | {b.customer.name} | {b.package.package_name} | {b.booking_status}").pack(side="left", padx=10)
            
            # Cancel Button
            ctk.CTkButton(row_frame, text="Cancel", width=60, fg_color="#dc3545", hover_color="#c82333",
                          command=lambda id=bid: self.cancel_booking_action(id)).pack(side="right", padx=5)
            
            # Check-in/Out Buttons
            ctk.CTkButton(row_frame, text="Check-In", width=60, command=lambda id=bid: self.check_in_action(id)).pack(side="right", padx=5)
            ctk.CTkButton(row_frame, text="Check-Out", width=60, command=lambda id=bid: self.check_out_action(id)).pack(side="right", padx=5)

    def cancel_booking_action(self, bid):
        if messagebox.askyesno("Confirm", f"Are you sure you want to cancel booking {bid}?"):
            try:
                self.system.cancel_booking(bid)
                self.show_bookings()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def check_in_action(self, bid):
        try:
            if self.system.check_in_booking(bid):
                messagebox.showinfo("Success", f"Booking {bid} checked in.")
                self.show_bookings()
            else:
                messagebox.showwarning("Failed", "Check-in failed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_out_action(self, bid):
        try:
            if self.system.check_out_booking(bid):
                messagebox.showinfo("Success", f"Booking {bid} checked out.")
                self.show_bookings()
            else:
                messagebox.showwarning("Failed", "Check-out failed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_hotels(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="Hotel Management", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        # Form Frame
        form_frame = ctk.CTkFrame(self.content_area)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Add New Hotel", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        entries = {}
        fields = [("Hotel ID", "hid"), ("Name", "name"), ("Location", "loc"), ("Room Type", "rtype"), ("Price", "price"), ("Available Rooms", "rooms")]
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label).grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=200)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            entries[key] = entry

        def add():
            try:
                self.system.add_hotel(
                    entries['hid'].get(), entries['name'].get(), entries['loc'].get(),
                    entries['rtype'].get(), float(entries['price'].get()), int(entries['rooms'].get())
                )
                messagebox.showinfo("Success", "Hotel added!")
                self.show_hotels()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(form_frame, text="Add Hotel", command=add, fg_color="green").grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        # List Frame
        list_frame = ctk.CTkFrame(self.content_area)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(list_frame, text="Hotels List", font=ctk.CTkFont(weight="bold")).pack(pady=5)

        for hid, h in self.system.hotels.items():
            row_frame = ctk.CTkFrame(list_frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            ctk.CTkLabel(row_frame, text=f"{h.hotel_id} | {h.hotel_name} ({h.location}) | {h.available_rooms} rooms left").pack(side="left", padx=10)

    def show_transports(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="Transportation Management", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        # Tabs for Add vs Search
        tabview = ctk.CTkTabview(self.content_area)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)
        tabview.add("Add Transport")
        tabview.add("Search & View")

        # Add Tab
        add_frame = tabview.tab("Add Transport")
        entries = {}
        fields = [("Transport ID", "tid"), ("Type", "type"), ("Source", "src"), ("Destination", "dest"), ("Fare", "fare"), ("Seats", "seats")]
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(add_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(add_frame, width=200)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[key] = entry

        def add():
            try:
                self.system.add_transport(
                    entries['tid'].get().strip(), entries['type'].get().strip(), entries['src'].get().strip(),
                    entries['dest'].get().strip(), float(entries['fare'].get()), int(entries['seats'].get())
                )
                messagebox.showinfo("Success", "Transport added!")
                self.show_transports()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(add_frame, text="Add Transport", command=add, fg_color="green").grid(row=len(fields), column=0, columnspan=2, pady=10)

        # Search Tab
        search_frame = tabview.tab("Search & View")
        search_input_frame = ctk.CTkFrame(search_frame)
        search_input_frame.pack(fill="x", padx=5, pady=5)

        src_entry = ctk.CTkEntry(search_input_frame, placeholder_text="Source")
        src_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        dest_entry = ctk.CTkEntry(search_input_frame, placeholder_text="Destination")
        dest_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        
        results_box = ctk.CTkTextbox(search_frame, height=200)
        results_box.pack(fill="x", padx=5, pady=5)

        def search():
            results_box.delete("1.0", "end")
            src = src_entry.get().strip()
            dest = dest_entry.get().strip()
            results = self.system.search_transports(src, dest)
            if results:
                results_box.insert("end", f"Results for '{src}' to '{dest}':\n")
                results_box.insert("end", "-"*40 + "\n")
                for t in results:
                    status = "Available" if t.available_seats > 0 else "FULL"
                    results_box.insert("end", f"{t.transport_id} | {t.transport_type} | {status} | Seats: {t.available_seats}\n")
            else:
                results_box.insert("end", f"No transports found for '{src}' to '{dest}'.\n")

        ctk.CTkButton(search_input_frame, text="Search", command=search).pack(side="left", padx=5, pady=5)

        # All Transports List
        ctk.CTkLabel(search_frame, text="All Registered Transports:", font=ctk.CTkFont(weight="bold")).pack(pady=(10,0))
        
        all_list_frame = ctk.CTkScrollableFrame(search_frame, height=200)
        all_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        for t in self.system.transports.values():
            status = "Available" if t.available_seats > 0 else "FULL"
            row = ctk.CTkFrame(all_list_frame)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{t.transport_id} | {t.transport_type} | {t.source} -> {t.destination} | {status} ({t.available_seats} seats)").pack(side="left", padx=10)

    def show_payments(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="Payment Management", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        # Form Frame
        form_frame = ctk.CTkFrame(self.content_area)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Process Payment", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        entries = {}
        fields = [("Payment ID", "pid"), ("Amount", "amt"), ("Mode", "mode"), ("Booking ID", "bid")]
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label).grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=200)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            entries[key] = entry

        def process():
            try:
                self.system.process_payment(
                    entries['pid'].get(), float(entries['amt'].get()), entries['mode'].get(), entries['bid'].get()
                )
                messagebox.showinfo("Success", "Payment processed!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(form_frame, text="Process Payment", command=process, fg_color="green").grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        # List Frame
        list_frame = ctk.CTkFrame(self.content_area)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(list_frame, text="Payment History", font=ctk.CTkFont(weight="bold")).pack(pady=5)

        for py_id, py in self.system.payments.items():
            row_frame = ctk.CTkFrame(list_frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            ctk.CTkLabel(row_frame, text=f"{py.payment_id} | ${py.amount:.2f} | {py.payment_mode} | Booking: {py.booking_id}").pack(side="left", padx=10)

    def show_schedules(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="Travel Schedule Management", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        # Form Frame
        form_frame = ctk.CTkFrame(self.content_area)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Add New Schedule", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        entries = {}
        fields = [("Schedule ID", "sid"), ("Departure (YYYY-MM-DD)", "dep"), ("Return (YYYY-MM-DD)", "ret"), ("Itinerary (comma separated)", "itin")]
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label).grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=200)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            entries[key] = entry

        def add():
            try:
                itin = [item.strip() for item in entries['itin'].get().split(',')]
                self.system.add_schedule(entries['sid'].get(), entries['dep'].get(), entries['ret'].get(), itin)
                messagebox.showinfo("Success", "Schedule added!")
                self.show_schedules()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(form_frame, text="Add Schedule", command=add, fg_color="green").grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        # List Frame
        list_frame = ctk.CTkFrame(self.content_area)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(list_frame, text="Schedules List", font=ctk.CTkFont(weight="bold")).pack(pady=5)

        for sid, s in self.system.schedules.items():
            row_frame = ctk.CTkFrame(list_frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            ctk.CTkLabel(row_frame, text=f"{s.schedule_id} | {s.departure_date} to {s.return_date} | Itinerary: {', '.join(s.itinerary)}").pack(side="left", padx=10)

    def show_reports(self):
        self.clear_content()
        ctk.CTkLabel(self.content_area, text="Report Generation", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        report_frame = ctk.CTkFrame(self.content_area)
        report_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(report_frame, text="Select Report Type", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)

        def generate(report_type_func, filename_prefix):
            filename = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=f"{filename_prefix}.csv")
            if filename:
                try:
                    report_type_func(filename)
                    messagebox.showinfo("Success", f"Report generated: {filename}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        ctk.CTkButton(report_frame, text="Booking Report", width=250, command=lambda: generate(self.system.generate_booking_report, "booking_report")).grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(report_frame, text="Revenue Report", width=250, command=lambda: generate(self.system.generate_revenue_report, "revenue_report")).grid(row=1, column=1, padx=20, pady=10)
        ctk.CTkButton(report_frame, text="Customer Report", width=250, command=lambda: generate(self.system.generate_customer_report, "customer_report")).grid(row=2, column=0, padx=20, pady=10)
        ctk.CTkButton(report_frame, text="Package Popularity", width=250, command=lambda: generate(self.system.generate_package_popularity_report, "package_popularity")).grid(row=2, column=1, padx=20, pady=10)
        ctk.CTkButton(report_frame, text="Cancellation Report", width=250, command=lambda: generate(self.system.generate_cancellation_report, "cancellation_report")).grid(row=3, column=0, padx=20, pady=10, columnspan=2)

if __name__ == "__main__":
    app = App()
    app.mainloop()
