class Transport:
    """Class representing a transportation service."""

    def __init__(self, transport_id: str, transport_type: str, source: str, destination: str, fare: float, available_seats: int):
        self.transport_id = transport_id
        self.transport_type = transport_type  # e.g., Bus, Flight, Train, Cab
        self.source = source
        self.destination = destination
        self.fare = fare
        self.available_seats = available_seats

    def book_transport(self, number_of_seats: int):
        if self.available_seats >= number_of_seats:
            self.available_seats -= number_of_seats
            print(f"Successfully booked {number_of_seats} seats for {self.transport_type} ({self.transport_id}).")
            return True
        else:
            print(f"Not enough seats available for {self.transport_type} ({self.transport_id}).")
            return False

    def cancel_transport(self, number_of_seats: int):
        self.available_seats += number_of_seats
        print(f"Cancelled {number_of_seats} seats for {self.transport_type} ({self.transport_id}).")

    def display_transport(self):
        print(f"--- Transport Details ---")
        print(f"ID: {self.transport_id}")
        print(f"Type: {self.transport_type}")
        print(f"Source: {self.source}")
        print(f"Destination: {self.destination}")
        print(f"Fare: ${self.fare:.2f}")
        print(f"Available Seats: {self.available_seats}")

    def __str__(self):
        return f"{self.transport_type} ({self.transport_id}): {self.source} to {self.destination} - ${self.fare:.2f}"

    def __repr__(self):
        return f"Transport(transport_id='{self.transport_id}', transport_type='{self.transport_type}', source='{self.source}', destination='{self.destination}', fare={self.fare}, available_seats={self.available_seats})"
