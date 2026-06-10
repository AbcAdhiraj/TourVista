class TourPackage:
    """Class representing a tour package."""

    def __init__(self, package_id: str, package_name: str, destination: str, duration: int, package_price: float, seasonal_discount: float = 0.0, hotel_id: str = None, transport_id: str = None):
        self.package_id = package_id
        self.package_name = package_name
        self.destination = destination
        self.duration = duration  # in days
        self.package_price = package_price
        self.seasonal_discount = seasonal_discount # in percentage
        self.hotel_id = hotel_id
        self.transport_id = transport_id

    @staticmethod
    def add_package(package_id: str, package_name: str, destination: str, duration: int, package_price: float, seasonal_discount: float = 0.0, hotel_id: str = None, transport_id: str = None):
        """Static method to create a new package."""
        return TourPackage(package_id, package_name, destination, duration, package_price, seasonal_discount, hotel_id, transport_id)

    def update_package(self, package_name=None, destination=None, duration=None, package_price=None, seasonal_discount=None, hotel_id=None, transport_id=None):
        if package_name:
            self.package_name = package_name
        if destination:
            self.destination = destination
        if duration:
            self.duration = duration
        if package_price:
            self.package_price = package_price
        if seasonal_discount is not None:
            self.seasonal_discount = seasonal_discount
        if hotel_id:
            self.hotel_id = hotel_id
        if transport_id:
            self.transport_id = transport_id
        print(f"Package {self.package_id} updated successfully.")

    def get_final_price(self) -> float:
        """Calculates the final price after applying seasonal discount."""
        from utils.helpers import TravelUtils
        return TravelUtils.calculate_discount(self.package_price, self.seasonal_discount)

    def display_package(self):
        print(f"--- Tour Package Details ---")
        print(f"ID: {self.package_id}")
        print(f"Name: {self.package_name}")
        print(f"Destination: {self.destination}")
        print(f"Duration: {self.duration} days")
        print(f"Base Price: ${self.package_price:.2f}")
        if self.seasonal_discount > 0:
            print(f"Seasonal Discount: {self.seasonal_discount}%")
            print(f"Final Price: ${self.get_final_price():.2f}")
        else:
            print(f"Final Price: ${self.package_price:.2f}")

    def __str__(self):
        return f"Package: {self.package_name} ({self.destination}, {self.duration} days) - ${self.get_final_price():.2f}"

    def __repr__(self):
        return f"TourPackage(package_id='{self.package_id}', package_name='{self.package_name}', destination='{self.destination}', duration={self.duration}, package_price={self.package_price}, seasonal_discount={self.seasonal_discount})"
