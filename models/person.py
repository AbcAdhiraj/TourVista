from abc import ABC, abstractmethod

class Person(ABC):
    """Abstract base class representing a person."""
    
    def __init__(self, person_id: str, name: str, email: str, mobile_number: str):
        self.person_id = person_id
        self.name = name
        self.email = email
        self.mobile_number = mobile_number

    @abstractmethod
    def display_details(self):
        """Display the person's details."""
        pass

    @abstractmethod
    def update_details(self, name=None, email=None, mobile_number=None):
        """Update the person's details."""
        pass

    def __str__(self):
        return f"ID: {self.person_id}, Name: {self.name}, Email: {self.email}, Mobile: {self.mobile_number}"

    def __repr__(self):
        return f"Person(person_id='{self.person_id}', name='{self.name}', email='{self.email}', mobile_number='{self.mobile_number}')"


class Customer(Person):
    """Class representing a customer, inheriting from Person."""

    def __init__(self, person_id: str, name: str, email: str, mobile_number: str, address: str):
        super().__init__(person_id, name, email, mobile_number)
        self.address = address
        self.booking_history = []  # List to store booking objects

    def display_details(self):
        print(f"--- Customer Details ---")
        print(f"ID: {self.person_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Mobile: {self.mobile_number}")
        print(f"Address: {self.address}")
        print(f"Booking History Count: {len(self.booking_history)}")

    def update_details(self, name=None, email=None, mobile_number=None, address=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if mobile_number:
            self.mobile_number = mobile_number
        if address:
            self.address = address
        print("Customer details updated successfully.")

    def book_package(self, package):
        # This will be implemented in the management layer
        pass

    def cancel_booking(self, booking_id):
        # This will be implemented in the management layer
        pass

    def view_bookings(self):
        if not self.booking_history:
            print("No booking history found.")
        else:
            print(f"--- Booking History for {self.name} ---")
            for booking in self.booking_history:
                print(booking)


class TravelAgent(Person):
    """Class representing a travel agent, inheriting from Person."""

    def __init__(self, person_id: str, name: str, email: str, mobile_number: str, department: str):
        super().__init__(person_id, name, email, mobile_number)
        self.agent_id = person_id # Using person_id as agent_id
        self.department = department

    def display_details(self):
        print(f"--- Travel Agent Details ---")
        print(f"Agent ID: {self.agent_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Mobile: {self.mobile_number}")
        print(f"Department: {self.department}")

    def update_details(self, name=None, email=None, mobile_number=None, department=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if mobile_number:
            self.mobile_number = mobile_number
        if department:
            self.department = department
        print("Travel Agent details updated successfully.")

    def create_package(self, package):
        # This will be implemented in the management layer
        pass

    def manage_bookings(self):
        # This will be implemented in the management layer
        pass

    def generate_reports(self):
        # This will be implemented in the management layer
        pass
