import json
import os
from datetime import datetime
from models.person import Customer, TravelAgent
from models.package import TourPackage
from models.hotel import Hotel
from models.transport import Transport
from models.booking import Booking
from models.payment import Payment
from models.schedule import TravelSchedule
from models.report import Report
from core.exceptions import (
    InvalidCustomerID, InvalidBookingID, PackageNotAvailable,
    HotelNotAvailable, InvalidPaymentAmount, IncorrectUserInput, TransportNotAvailable
)

class TravelManagementSystem:
    """The main controller class for the Tour & Travel Booking System."""

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.customers = {}   # customer_id -> Customer object
        self.packages = {}    # package_id -> TourPackage object
        self.bookings = {}    # booking_id -> Booking object
        self.hotels = {}      # hotel_id -> Hotel object
        self.transports = {}  # transport_id -> Transport object
        self.payments = {}    # payment_id -> Payment object
        self.schedules = {}   # schedule_id -> TravelSchedule object

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    # --- Customer Management ---

    def register_customer(self, customer_id, name, email, mobile_number, address):
        if customer_id in self.customers:
            print(f"Error: Customer with ID {customer_id} already exists.")
            return False
        new_customer = Customer(customer_id, name, email, mobile_number, address)
        self.customers[customer_id] = new_customer
        print(f"Customer {name} registered successfully.")
        return True

    def get_customer(self, customer_id):
        if customer_id not in self.customers:
            raise InvalidCustomerID(f"Customer with ID {customer_id} not found.")
        return self.customers[customer_id]

    # --- Package Management ---

    def create_package(self, package_id, package_name, destination, duration, package_price, hotel_id=None, transport_id=None):
        if package_id in self.packages:
            print(f"Error: Package with ID {package_id} already exists.")
            return False
        new_package = TourPackage(package_id, package_name, destination, duration, package_price, hotel_id=hotel_id, transport_id=transport_id)
        self.packages[package_id] = new_package
        print(f"Tour package '{package_name}' created successfully.")
        return True

    def get_package(self, package_id):
        if package_id not in self.packages:
            raise PackageNotAvailable(f"Package with ID {package_id} not found.")
        return self.packages[package_id]

    # --- Booking Management ---

    def create_booking(self, booking_id, customer_id, package_id, booking_date=None):
        customer = self.get_customer(customer_id)
        package = self.get_package(package_id)
        
        if booking_date is None:
            booking_date = datetime.now()

        # Availability check and reservation
        if package.hotel_id:
            hotel = self.get_hotel(package.hotel_id)
            if not hotel.check_availability():
                raise HotelNotAvailable(f"Hotel {hotel.hotel_name} has no more rooms available.")
            hotel.reserve_room(1)
        
        if package.transport_id:
            transport = self.get_transport(package.transport_id)
            if not transport or transport.available_seats <= 0:
                # If hotel was already reserved, we should release it if transport fails
                if package.hotel_id:
                    self.get_hotel(package.hotel_id).release_rooms(1)
                raise TransportNotAvailable(f"Transport {package.transport_id} is not available.")
            transport.book_transport(1)

        new_booking = Booking(booking_id, customer, package, booking_date)
        self.bookings[booking_id] = new_booking
        customer.booking_history.append(new_booking)
        print(f"Booking {booking_id} created for customer {customer.name}.")
        return True

    def cancel_booking(self, booking_id):
        if booking_id not in self.bookings:
            raise InvalidBookingID(f"Booking with ID {booking_id} not found.")
        
        booking = self.bookings[booking_id]
        if booking.booking_status != "Cancelled":
            package = booking.package
            if package.hotel_id:
                self.get_hotel(package.hotel_id).release_rooms(1)
            if package.transport_id:
                transport = self.get_transport(package.transport_id)
                if transport:
                    transport.cancel_transport(1)
            
            booking.cancel_booking()
        return True

    def check_in_booking(self, booking_id):
        """Checks in a booking."""
        if booking_id not in self.bookings:
            raise InvalidBookingID(f"Booking with ID {booking_id} not found.")
        
        booking = self.bookings[booking_id]
        if booking.check_in():
            return True
        return False

    def check_out_booking(self, booking_id):
        """Checks out a booking."""
        if booking_id not in self.bookings:
            raise InvalidBookingID(f"Booking with ID {booking_id} not found.")
        
        booking = self.bookings[booking_id]
        if booking.check_out():
            return True
        return False

    def process_payment(self, payment_id, amount, payment_mode, booking_id):
        if booking_id not in self.bookings:
            raise InvalidBookingID(f"Cannot process payment. Booking {booking_id} not found.")
        
        if amount <= 0:
            raise InvalidPaymentAmount("Payment amount must be greater than zero.")
        
        booking = self.bookings[booking_id]
        payment_date = datetime.now()
        new_payment = Payment(payment_id, amount, payment_mode, payment_date, booking_id)
        
        # In a real system, we'd verify if amount matches booking price
        # For this simulation, we'll just proceed.
        
        self.payments[payment_id] = new_payment
        print(f"Payment {payment_id} processed for Booking {booking_id}.")
        return True

    def process_refund(self, refund_id, amount, booking_id):
        """Processes a refund for a booking."""
        if booking_id not in self.bookings:
            raise InvalidBookingID(f"Cannot process refund. Booking {booking_id} not found.")
        
        if amount <= 0:
            raise InvalidPaymentAmount("Refund amount must be greater than zero.")
        
        booking = self.bookings[booking_id]
        
        # In a real system, we'd check if enough payments were made
        
        refund_date = datetime.now()
        # For simulation, we'll just record it.
        # In a real system, we'd have a Refund class.
        print(f"Refund {refund_id} of ${amount:.2f} processed for Booking {booking_id}.")
        return True


    # --- Hotel Management (Simplified) ---

    def add_hotel(self, hotel_id, hotel_name, location, room_type, room_price, available_rooms):
        if hotel_id in self.hotels:
            print(f"Error: Hotel with ID {hotel_id} already exists.")
            return False
        new_hotel = Hotel(hotel_id, hotel_name, location, room_type, room_price, available_rooms)
        self.hotels[hotel_id] = new_hotel
        print(f"Hotel {hotel_name} added successfully.")
        return True

    def get_hotel(self, hotel_id):
        if hotel_id not in self.hotels:
            raise HotelNotAvailable(f"Hotel with ID {hotel_id} not found.")
        return self.hotels[hotel_id]

    # --- Transportation Management (Simplified) ---

    def add_transport(self, transport_id, transport_type, source, destination, fare, available_seats):
        if transport_id in self.transports:
            print(f"Error: Transport with ID {transport_id} already exists.")
            return False
        new_transport = Transport(transport_id, transport_type, source, destination, fare, available_seats)
        self.transports[transport_id] = new_transport
        print(f"Transport {transport_type} ({transport_id}) added successfully.")
        return True

    def get_transport(self, transport_id):
        if transport_id not in self.transports:
            print(f"Transport with ID {transport_id} not found.")
            return None
        return self.transports[transport_id]

    def search_transports(self, source, destination):
        """Searches for transports between source and destination."""
        return [t for t in self.transports.values() if t.source.lower().strip() == source.lower().strip() and t.destination.lower().strip() == destination.lower().strip()]

    # --- Schedule Management ---

    def add_schedule(self, schedule_id, departure_date, return_date, itinerary):
        if schedule_id in self.schedules:
            print(f"Error: Schedule with ID {schedule_id} already exists.")
            return False
        new_schedule = TravelSchedule(schedule_id, departure_date, return_date, itinerary)
        self.schedules[schedule_id] = new_schedule
        print(f"Travel schedule {schedule_id} added successfully.")
        return True

    def get_schedule(self, schedule_id):
        if schedule_id not in self.schedules:
            raise ValueError(f"Schedule with ID {schedule_id} not found.")
        return self.schedules[schedule_id]

    def list_schedules(self):
        return list(self.schedules.values())

    def save_schedules(self):
        # I should probably add this to save_data as well.
        pass

    # --- Report Management ---

    def get_sorted_packages(self, sort_by="price"):
        """Returns a list of packages sorted by the given attribute using lambdas."""
        if sort_by == "price":
            return sorted(self.packages.values(), key=lambda p: p.package_price)
        elif sort_by == "name":
            return sorted(self.packages.values(), key=lambda p: p.package_name)
        elif sort_by == "duration":
            return sorted(self.packages.values(), key=lambda p: p.duration)
        else:
            return list(self.packages.values())

    def get_available_hotels(self):
        """Returns a list of available hotels using list comprehension."""
        return [h for h in self.hotels.values() if h.available_rooms > 0]

    def get_available_transports(self):
        """Returns a list of available transports using list comprehension."""
        return [t for t in self.transports.values() if t.available_seats > 0]

    def search_customer_recursive(self, search_term, customers_list=None):
        """Recursively searches for customers by name or ID."""
        if customers_list is None:
            customers_list = list(self.customers.values())
        
        results = []
        for customer in customers_list:
            if search_term.lower() in customer.name.lower() or search_term.lower() in customer.person_id.lower():
                results.append(customer)
            # In a real recursive scenario, we might traverse a tree, but here we just demonstrate the technique
            # or we could implement it by splitting the list and recursing.
        
        # To truly demonstrate recursion as requested:
        def _recursive_search(lst):
            if not lst:
                return []
            first = lst[0]
            rest = lst[1:]
            if search_term.lower() in first.name.lower() or search_term.lower() in first.person_id.lower():
                return [first] + _recursive_search(rest)
            else:
                return _recursive_search(rest)
        
        return _recursive_search(customers_list)

    def generate_booking_report(self, filename):
        report = Report("REP_B_001", "Booking Report")
        def data_generator():
            for b_id, b in self.bookings.items():
                yield {
                    "booking_id": b.booking_id,
                    "customer_name": b.customer.name,
                    "package_name": b.package.package_name,
                    "date": b.booking_date.strftime('%Y-%m-%d'),
                    "status": b.booking_status
                }
        report.export_report(data_generator(), filename)

    def generate_revenue_report(self, filename):
        report = Report("REP_R_001", "Revenue Report")
        def data_generator():
            for py_id, py in self.payments.items():
                yield {
                    "payment_id": py.payment_id,
                    "amount": py.amount,
                    "payment_mode": py.payment_mode,
                    "payment_date": py.payment_date.strftime('%Y-%m-%d %H:%M:%S'),
                    "booking_id": py.booking_id
                }
        report.export_report(data_generator(), filename)

    def generate_customer_report(self, filename):
        report = Report("REP_C_001", "Customer Report")
        def data_generator():
            for c_id, c in self.customers.items():
                yield {
                    "person_id": c.person_id,
                    "name": c.name,
                    "email": c.email,
                    "mobile_number": c.mobile_number,
                    "address": c.address
                }
        report.export_report(data_generator(), filename)

    def generate_package_popularity_report(self, filename):
        report = Report("REP_P_001", "Package Popularity Report")
        package_counts = {}
        for b in self.bookings.values():
            pid = b.package.package_id
            package_counts[pid] = package_counts.get(pid, 0) + 1
        
        def data_generator():
            for pid, count in package_counts.items():
                package = self.packages.get(pid)
                yield {
                    "package_id": pid,
                    "package_name": package.package_name if package else "Unknown",
                    "booking_count": count
                }
        report.export_report(data_generator(), filename)

    def generate_cancellation_report(self, filename):
        report = Report("REP_CAN_001", "Cancellation Report")
        def data_generator():
            for b_id, b in self.bookings.items():
                if b.booking_status == "Cancelled":
                    yield {
                        "booking_id": b.booking_id,
                        "customer_name": b.customer.name,
                        "package_name": b.package.package_name,
                        "date": b.booking_date.strftime('%Y-%m-%d'),
                        "status": b.booking_status
                    }
        report.export_report(data_generator(), filename)

    def save_data(self):
        """Saves all current data to JSON files."""
        try:
            # Saving customers
            customer_data = []
            for c in self.customers.values():
                customer_data.append({
                    "person_id": c.person_id,
                    "name": c.name,
                    "email": c.email,
                    "mobile_number": c.mobile_number,
                    "address": c.address
                })
            with open(os.path.join(self.data_dir, "customers.json"), 'w') as f:
                json.dump(customer_data, f, indent=4)

            # Saving packages
            package_data = []
            for p in self.packages.values():
                package_data.append({
                    "package_id": p.package_id,
                    "package_name": p.package_name,
                    "destination": p.destination,
                    "duration": p.duration,
                    "package_price": p.package_price,
                    "hotel_id": p.hotel_id,
                    "transport_id": p.transport_id
                })
            with open(os.path.join(self.data_dir, "packages.json"), 'w') as f:
                json.dump(package_data, f, indent=4)

            # Saving bookings
            booking_data = []
            for b in self.bookings.values():
                booking_data.append({
                    "booking_id": b.booking_id,
                    "customer_id": b.customer.person_id,
                    "package_id": b.package.package_id,
                    "booking_date": b.booking_date.strftime('%Y-%m-%d %H:%M:%S'),
                    "booking_status": b.booking_status
                })
            with open(os.path.join(self.data_dir, "bookings.json"), 'w') as f:
                json.dump(booking_data, f, indent=4)

            # Saving hotels
            hotel_data = []
            for h in self.hotels.values():
                hotel_data.append({
                    "hotel_id": h.hotel_id,
                    "hotel_name": h.hotel_name,
                    "location": h.location,
                    "room_type": h.room_type,
                    "room_price": h.room_price,
                    "available_rooms": h.available_rooms
                })
            with open(os.path.join(self.data_dir, "hotels.json"), 'w') as f:
                json.dump(hotel_data, f, indent=4)

            # Saving transports
            transport_data = []
            for t in self.transports.values():
                transport_data.append({
                    "transport_id": t.transport_id,
                    "transport_type": t.transport_type,
                    "source": t.source,
                    "destination": t.destination,
                    "fare": t.fare,
                    "available_seats": t.available_seats
                })
            with open(os.path.join(self.data_dir, "transports.json"), 'w') as f:
                json.dump(transport_data, f, indent=4)

            # Saving payments
            payment_data = []
            for py in self.payments.values():
                payment_data.append({
                    "payment_id": py.payment_id,
                    "amount": py.amount,
                    "payment_mode": py.payment_mode,
                    "payment_date": py.payment_date.strftime('%Y-%m-%d %H:%M:%S'),
                    "booking_id": py.booking_id
                })
            with open(os.path.join(self.data_dir, "payments.json"), 'w') as f:
                json.dump(payment_data, f, indent=4)

            # Saving schedules
            schedule_data = []
            for s in self.schedules.values():
                schedule_data.append({
                    "schedule_id": s.schedule_id,
                    "departure_date": s.departure_date,
                    "return_date": s.return_date,
                    "itinerary": s.itinerary
                })
            with open(os.path.join(self.data_dir, "schedules.json"), 'w') as f:
                json.dump(schedule_data, f, indent=4)

            print("All data saved successfully.")
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def load_data(self):
        """Loads all data from JSON files."""
        try:
            # Loading customers
            customers_file = os.path.join(self.data_dir, "customers.json")
            if os.path.exists(customers_file):
                with open(customers_file, 'r') as f:
                    customer_list = json.load(f)
                    for c_info in customer_list:
                        new_c = Customer(
                            c_info['person_id'],
                            c_info['name'],
                            c_info['email'],
                            c_info['mobile_number'],
                            c_info['address']
                        )
                        self.customers[new_c.person_id] = new_c

            # Loading packages
            packages_file = os.path.join(self.data_dir, "packages.json")
            if os.path.exists(packages_file):
                with open(packages_file, 'r') as f:
                    package_list = json.load(f)
                    for p_info in package_list:
                        new_p = TourPackage(
                            p_info['package_id'],
                            p_info['package_name'],
                            p_info['destination'],
                            p_info['duration'],
                            p_info['package_price'],
                            hotel_id=p_info.get('hotel_id'),
                            transport_id=p_info.get('transport_id')
                        )
                        self.packages[new_p.package_id] = new_p

            # Loading hotels
            hotels_file = os.path.join(self.data_dir, "hotels.json")
            if os.path.exists(hotels_file):
                with open(hotels_file, 'r') as f:
                    hotel_list = json.load(f)
                    for h_info in hotel_list:
                        new_h = Hotel(
                            h_info['hotel_id'],
                            h_info['hotel_name'],
                            h_info['location'],
                            h_info['room_type'],
                            h_info['room_price'],
                            h_info['available_rooms']
                        )
                        self.hotels[new_h.hotel_id] = new_h

            # Loading transports
            transports_file = os.path.join(self.data_dir, "transports.json")
            if os.path.exists(transports_file):
                with open(transports_file, 'r') as f:
                    transport_list = json.load(f)
                    for t_info in transport_list:
                        new_t = Transport(
                            t_info['transport_id'],
                            t_info['transport_type'],
                            t_info['source'],
                            t_info['destination'],
                            t_info['fare'],
                            t_info['available_seats']
                        )
                        self.transports[new_t.transport_id] = new_t

            # Loading bookings
            bookings_file = os.path.join(self.data_dir, "bookings.json")
            if os.path.exists(bookings_file):
                with open(bookings_file, 'r') as f:
                    booking_list = json.load(f)
                    for b_info in booking_list:
                        customer = self.customers.get(b_info['customer_id'])
                        package = self.packages.get(b_info['package_id'])
                        if customer and package:
                            booking_date = datetime.strptime(b_info['booking_date'], '%Y-%m-%d %H:%M:%S')
                            new_b = Booking(
                                b_info['booking_id'],
                                customer,
                                package,
                                booking_date,
                                b_info['booking_status']
                            )
                            self.bookings[new_b.booking_id] = new_b
                            customer.booking_history.append(new_b)

            # Loading payments
            payments_file = os.path.join(self.data_dir, "payments.json")
            if os.path.exists(payments_file):
                with open(payments_file, 'r') as f:
                    payment_list = json.load(f)
                    for py_info in payment_list:
                        booking = self.bookings.get(py_info['booking_id'])
                        if booking:
                            payment_date = datetime.strptime(py_info['payment_date'], '%Y-%m-%d %H:%M:%S')
                            new_py = Payment(
                                py_info['payment_id'],
                                py_info['amount'],
                                py_info['payment_mode'],
                                payment_date,
                                py_info['booking_id']
                            )
                            self.payments[new_py.payment_id] = new_py

            # Loading schedules
            schedules_file = os.path.join(self.data_dir, "schedules.json")
            if os.path.exists(schedules_file):
                with open(schedules_file, 'r') as f:
                    schedule_list = json.load(f)
                    for s_info in schedule_list:
                        new_s = TravelSchedule(
                            s_info['schedule_id'],
                            s_info['departure_date'],
                            s_info['return_date'],
                            s_info['itinerary']
                        )
                        self.schedules[new_s.schedule_id] = new_s

            print("All data loaded successfully.")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
