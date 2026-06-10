class TourTravelException(Exception):
    """Base exception class for the Tour & Travel System."""
    pass

class InvalidCustomerID(TourTravelException):
    """Raised when the customer ID is invalid."""
    pass

class InvalidBookingID(TourTravelException):
    """Raised when the booking ID is invalid."""
    pass

class PackageNotAvailable(TourTravelException):
    """Raised when a package is not available."""
    pass

class HotelNotAvailable(TourTravelException):
    """Raised when a hotel is not available."""
    pass

class TransportNotAvailable(TourTravelException):
    """Raised when a transport is not available."""
    pass

class InvalidPaymentAmount(TourTravelException):
    """Raised when the payment amount is invalid."""
    pass

class FileNotFoundErrorCustom(TourTravelException):
    """Raised when a data file is not found."""
    pass

class IncorrectUserInput(TourTravelException):
    """Raised when the user input is incorrect."""
    pass
