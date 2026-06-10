class TravelUtils:
    """Utility class for static and class methods."""

    @staticmethod
    def calculate_discount(price: float, discount_percentage: float) -> float:
        """Calculates the discounted price."""
        return price * (1 - (discount_percentage / 100))

    @staticmethod
    def calculate_fare(base_fare: float, extra_charges: float) -> float:
        """Calculates the total fare."""
        return base_fare + extra_charges

    @classmethod
    def get_agency_statistics(cls, total_customers, total_packages, total_bookings):
        """Generates simple statistics for the travel agency."""
        stats = {
            "total_customers": total_customers,
            "total_packages": total_packages,
            "total_bookings": total_bookings,
            "customer_to_booking_ratio": total_bookings / total_customers if total_customers > 0 else 0
        }
        return stats
