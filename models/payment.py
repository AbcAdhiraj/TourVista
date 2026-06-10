from datetime import datetime

class Payment:
    """Class representing a payment."""

    def __init__(self, payment_id: str, amount: float, payment_mode: str, payment_date: datetime, booking_id: str):
        self.payment_id = payment_id
        self.amount = amount
        self.payment_mode = payment_mode  # e.g., Credit Card, Cash, UPI
        self.payment_date = payment_date
        self.booking_id = booking_id

    def process_payment(self):
        # This will be implemented in the management layer
        print(f"Payment of ${self.amount:.2f} processed via {self.payment_mode} for Booking {self.booking_id}.")
        return True

    def generate_invoice(self):
        print(f"--- Invoice ---")
        print(f"Payment ID: {self.payment_id}")
        print(f"Booking ID: {self.booking_id}")
        print(f"Amount Paid: ${self.amount:.2f}")
        print(f"Date: {self.payment_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Mode: {self.payment_mode}")
        print(f"----------------")

    def refund_payment(self, amount: float):
        print(f"Refund of ${amount:.2f} processed for Payment {self.payment_id}.")
        return True

    def __str__(self):
        return f"Payment ID: {self.payment_id}, Amount: ${self.amount:.2f}, Mode: {self.payment_mode}, Date: {self.payment_date.strftime('%Y-%m-%d')}"

    def __repr__(self):
        return f"Payment(payment_id='{self.payment_id}', amount={self.amount}, payment_mode='{self.payment_mode}', payment_date={self.payment_date}, booking_id='{self.booking_id}')"
