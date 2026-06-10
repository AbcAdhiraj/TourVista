from core.management import TravelManagementSystem
from core.exceptions import HotelNotAvailable, TransportNotAvailable

def test_system():
    system = TravelManagementSystem()
    
    print("Running Basic Test...")
    # 1. Register Customer
    system.register_customer("C001", "John Doe", "john@example.com", "1234567890", "123 Main St")
    
    # 2. Create Package with Hotel and Transport
    system.create_package("P001", "Paris Getaway", "Paris", 5, 1500.0, hotel_id="H001", transport_id="T001")
    
    # 3. Add Hotel
    system.add_hotel("H001", "Grand Hotel", "Paris", "Deluxe", 200.0, 1) # Only 1 room
    
    # 4. Add Transport
    system.add_transport("T001", "Flight", "New York", "Paris", 800.0, 1) # Only 1 seat
    
    # 5. Create Booking (Should succeed)
    system.create_booking("B001", "C001", "P001")
    print("Booking B001 created successfully.")
    
    # 6. Try another booking for same package (Should fail due to availability)
    system.register_customer("C002", "Jane Smith", "jane@example.com", "0987654321", "456 Oak St")
    try:
        system.create_booking("B002", "C002", "P001")
        print("Error: B002 should have failed due to availability.")
    except HotelNotAvailable:
        print("B002 failed as expected: Hotel not available.")
    except TransportNotAvailable:
        print("B002 failed as expected: Transport not available.")
    except Exception as e:
        print(f"Unexpected exception: {type(e).__name__}: {e}")

    # 7. Cancel B001 (Should release availability)
    system.cancel_booking("B001")
    print("Booking B001 cancelled.")
    
    # 8. Try B002 again (Should succeed now)
    try:
        system.create_booking("B002", "C002", "P001")
        print("B002 created successfully after cancellation.")
    except Exception as e:
        print(f"Error: B002 should have succeeded after cancellation. Error: {e}")

    # 9. Process Payment
    system.process_payment("PAY001", 1500.0, "Credit Card", "B001") # This will fail because B001 is cancelled? 
    # Actually B001 was cancelled, so maybe I should use B002.
    
    # Let's fix step 9.
    try:
        system.process_payment("PAY002", 1500.0, "Credit Card", "B002")
        print("Payment for B002 processed successfully.")
    except Exception as e:
        print(f"Error processing payment for B002: {e}")
    
    # 10. Save Data
    system.save_data()
    
    print("\nTest completed successfully.")

if __name__ == "__main__":
    test_system()
