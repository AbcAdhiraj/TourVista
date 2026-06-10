class TravelSchedule:
    """Class representing a travel schedule."""

    def __init__(self, schedule_id: str, departure_date: str, return_date: str, itinerary: list):
        self.schedule_id = schedule_id
        self.departure_date = departure_date
        self.return_date = return_date
        self.itinerary = itinerary  # List of strings/activities

    def create_schedule(self, schedule_id: str, departure_date: str, return_date: str, itinerary: list):
        self.schedule_id = schedule_id
        self.departure_date = departure_date
        self.return_date = return_date
        self.itinerary = itinerary
        print(f"Schedule {self.schedule_id} created.")

    def update_schedule(self, departure_date=None, return_date=None, itinerary=None):
        if departure_date:
            self.departure_date = departure_date
        if return_date:
            self.return_date = return_date
        if itinerary:
            self.itinerary = itinerary
        print(f"Schedule {self.schedule_id} updated.")

    def display_schedule(self):
        print(f"--- Travel Schedule ---")
        print(f"Schedule ID: {self.schedule_id}")
        print(f"Departure: {self.departure_date}")
        print(f"Return: {self.return_date}")
        print(f"Itinerary:")
        if not self.itinerary:
            print("  (No itinerary details)")
        for item in self.itinerary:
            print(f"  - {item}")

    def __str__(self):
        return f"Schedule {self.schedule_id}: {self.departure_date} to {self.return_date}"

    def __repr__(self):
        return f"TravelSchedule(schedule_id='{self.schedule_id}', departure_date='{self.departure_date}', return_date='{self.return_date}', itinerary={self.itinerary})"
