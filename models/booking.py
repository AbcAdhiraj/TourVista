from datetime import datetime

class Booking:
    """Class representing a booking."""

    def __init__(self, booking_id: str, customer, package, booking_date: datetime, booking_status: str = "Confirmed"):
        self.booking_id = booking_id
        self.customer = customer  # Customer object
        self.package = package    # TourPackage object
        self.booking_date = booking_date
        self.booking_status = booking_status  # Confirmed, CheckedIn, CheckedOut, Cancelled, Pending

    def create_booking(self):
        # Conceptually, this is handled by the management system
        pass

    def cancel_booking(self):
        self.booking_status = "Cancelled"
        print(f"Booking {self.booking_id} has been cancelled.")

    def confirm_booking(self):
        self.booking_status = "Confirmed"
        print(f"Booking {self.booking_id} has been confirmed.")

    def check_in(self):
        """Changes booking status to CheckedIn."""
        if self.booking_status == "Confirmed":
            self.booking_status = "CheckedIn"
            print(f"Booking {self.booking_id} checked in successfully.")
            return True
        else:
            print(f"Booking {self.booking_id} cannot be checked in from status {self.booking_status}.")
            return False

    def check_out(self):
        """Changes booking status to CheckedOut."""
        if self.booking_status == "CheckedIn":
            self.booking_status = "CheckedOut"
            print(f"Booking {self.booking_id} checked out successfully.")
            return True
        else:
            print(f"Booking {self.booking_id} cannot be checked out from status {self.booking_status}.")
            return False

    def display_booking(self):
        print(f"--- Booking Details ---")
        print(f"Booking ID: {self.booking_id}")
        print(f"Customer: {self.customer.name}")
        print(f"Package: {self.package.package_name}")
        print(f"Date: {self.booking_date.strftime('%Y-%m-%d')}")
        print(f"Status: {self.booking_status}")

    def __str__(self):
        return f"Booking ID: {self.booking_id}, Customer: {self.customer.name}, Package: {self.package.package_name}, Status: {self.booking_status}"

    def __repr__(self):
        return f"Booking(booking_id='{self.booking_id}', customer={self.customer}, package={self.package}, booking_date={self.booking_date}, booking_status='{self.booking_status}')"
