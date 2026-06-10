class Hotel:
    """Class representing a hotel."""

    def __init__(self, hotel_id: str, hotel_name: str, location: str, room_type: str, room_price: float, available_rooms: int):
        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self.location = location
        self.room_type = room_type
        self.room_price = room_price
        self.available_rooms = available_rooms

    def check_availability(self):
        return self.available_rooms > 0

    def reserve_room(self, number_of_rooms: int):
        if self.available_rooms >= number_of_rooms:
            self.available_rooms -= number_of_rooms
            print(f"Successfully reserved {number_of_rooms} rooms at {self.hotel_name}.")
            return True
        else:
            print(f"Not enough rooms available at {self.hotel_name}.")
            return False

    def release_rooms(self, number_of_rooms: int):
        self.available_rooms += number_of_rooms
        print(f"Released {number_of_rooms} rooms at {self.hotel_name}.")

    def display_hotel(self):
        print(f"--- Hotel Details ---")
        print(f"ID: {self.hotel_id}")
        print(f"Name: {self.hotel_name}")
        print(f"Location: {self.location}")
        print(f"Room Type: {self.room_type}")
        print(f"Price per Room: ${self.room_price:.2f}")
        print(f"Available Rooms: {self.available_rooms}")

    def __str__(self):
        return f"Hotel: {self.hotel_name} ({self.location}, {self.room_type}) - ${self.room_price:.2f}"

    def __repr__(self):
        return f"Hotel(hotel_id='{self.hotel_id}', hotel_name='{self.hotel_name}', location='{self.location}', room_type='{self.room_type}', room_price={self.room_price}, available_rooms={self.available_rooms})"
