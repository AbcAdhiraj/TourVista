import sys
from core.management import TravelManagementSystem
from core.exceptions import TourTravelException

def main_menu():
    system = TravelManagementSystem()
    system.load_data()

    while True:
        print("\n--- TOUR & TRAVEL BOOKING SYSTEM ---")
        print("1. Customer Management")
        print("2. Tour Package Management")
        print("3. Booking Management")
        print("4. Hotel Reservation Management")
        print("5. Transportation Management")
        print("6. Payment Management")
        print("7. Travel Schedule Management")
        print("8. Report Generation")
        print("9. Save Data")
        print("10. Load Data")
        print("11. Exit")
        
        choice = input("\nEnter your choice: ")
        
        try:
            if choice == '1':
                customer_menu(system)
            elif choice == '2':
                package_menu(system)
            elif choice == '3':
                booking_menu(system)
            elif choice == '4':
                hotel_menu(system)
            elif choice == '5':
                transport_menu(system)
            elif choice == '6':
                payment_menu(system)
            elif choice == '7':
                schedule_menu(system)
            elif choice == '8':
                report_menu(system)
            elif choice == '9':
                system.save_data()
            elif choice == '10':
                system.load_data()
            elif choice == '11':
                system.save_data()
                print("Exiting system. Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")
        except TourTravelException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def customer_menu(system):
    print("\n--- Customer Management ---")
    print("1. Register Customer")
    print("2. View Customer Details")
    print("3. View Booking History")
    print("4. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        cid = input("Enter Customer ID: ")
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        mobile = input("Enter Mobile: ")
        address = input("Enter Address: ")
        system.register_customer(cid, name, email, mobile, address)
    elif choice == '2':
        cid = input("Enter Customer ID: ")
        customer = system.get_customer(cid)
        customer.display_details()
    elif choice == '3':
        cid = input("Enter Customer ID: ")
        customer = system.get_customer(cid)
        customer.view_bookings()

def package_menu(system):
    print("\n--- Tour Package Management ---")
    print("1. Create Package")
    print("2. View All Packages")
    print("3. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        pid = input("Enter Package ID: ")
        name = input("Enter Package Name: ")
        dest = input("Enter Destination: ")
        dur = int(input("Enter Duration (days): "))
        price = float(input("Enter Price: "))
        system.create_package(pid, name, dest, dur, price)
    elif choice == '2':
        print("\nAvailable Packages:")
        for p in system.packages.values():
            print(p)

def booking_menu(system):
    print("\n--- Booking Management ---")
    print("1. Create Booking")
    print("2. Cancel Booking")
    print("3. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        bid = input("Enter Booking ID: ")
        cid = input("Enter Customer ID: ")
        pid = input("Enter Package ID: ")
        system.create_booking(bid, cid, pid)
    elif choice == '2':
        bid = input("Enter Booking ID to cancel: ")
        system.cancel_booking(bid)

def hotel_menu(system):
    print("\n--- Hotel Reservation Management ---")
    print("1. Add Hotel")
    print("2. View All Hotels")
    print("3. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        hid = input("Enter Hotel ID: ")
        name = input("Enter Hotel Name: ")
        loc = input("Enter Location: ")
        rtype = input("Enter Room Type: ")
        price = float(input("Enter Room Price: "))
        rooms = int(input("Enter Available Rooms: "))
        system.add_hotel(hid, name, loc, rtype, price, rooms)
    elif choice == '2':
        print("\nAvailable Hotels:")
        for h in system.hotels.values():
            print(h)

def transport_menu(system):
    print("\n--- Transportation Management ---")
    print("1. Add Transport")
    print("2. View All Transports")
    print("3. Search Transports")
    print("4. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        tid = input("Enter Transport ID: ")
        ttype = input("Enter Transport Type (Bus/Flight/Train/Cab): ")
        src = input("Enter Source: ")
        dest = input("Enter Destination: ")
        fare = float(input("Enter Fare: "))
        seats = int(input("Enter Available Seats: "))
        system.add_transport(tid, ttype, src, dest, fare, seats)
    elif choice == '2':
        print("\nAvailable Transports:")
        for t in system.transports.values():
            print(t)
    elif choice == '3':
        src = input("Enter Source: ")
        dest = input("Enter Destination: ")
        results = system.search_transports(src, dest)
        if results:
            print("\nAvailable Transports:")
            for t in results:
                print(t)
        else:
            print("No available transports found for this route.")

def payment_menu(system):
    print("\n--- Payment Management ---")
    print("1. Process Payment")
    print("2. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        payid = input("Enter Payment ID: ")
        amount = float(input("Enter Amount: "))
        mode = input("Enter Payment Mode (Cash/Card/UPI): ")
        bid = input("Enter Booking ID: ")
        system.process_payment(payid, amount, mode, bid)

def schedule_menu(system):
    print("\n--- Travel Schedule Management ---")
    print("1. Add Schedule")
    print("2. View All Schedules")
    print("3. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        sid = input("Enter Schedule ID: ")
        dep_date = input("Enter Departure Date (YYYY-MM-DD): ")
        ret_date = input("Enter Return Date (YYYY-MM-DD): ")
        itinerary_str = input("Enter Itinerary (comma separated activities): ")
        itinerary = [item.strip() for item in itinerary_str.split(',')]
        system.add_schedule(sid, dep_date, ret_date, itinerary)
    elif choice == '2':
        print("\nAvailable Schedules:")
        for s in system.list_schedules():
            print(s)

def report_menu(system):
    print("\n--- Report Generation ---")
    print("1. Booking Report (CSV)")
    print("2. Revenue Report (CSV)")
    print("3. Customer Report (CSV)")
    print("4. Package Popularity Report (CSV)")
    print("5. Cancellation Report (CSV)")
    print("6. Back")
    
    choice = input("Enter choice: ")
    if choice == '1':
        filename = input("Enter filename (e.g., reports/booking_report.csv): ")
        if not filename.endswith('.csv'):
            filename += '.csv'
        system.generate_booking_report(filename)
    elif choice == '2':
        filename = input("Enter filename (e.g., reports/revenue_report.csv): ")
        if not filename.endswith('.csv'):
            filename += '.csv'
        system.generate_revenue_report(filename)
    elif choice == '3':
        filename = input("Enter filename (e.g., reports/customer_report.csv): ")
        if not filename.endswith('.csv'):
            filename += '.csv'
        system.generate_customer_report(filename)
    elif choice == '4':
        filename = input("Enter filename (e.g., reports/package_popularity_report.csv): ")
        if not filename.endswith('.csv'):
            filename += '.csv'
        system.generate_package_popularity_report(filename)
    elif choice == '5':
        filename = input("Enter filename (e.g., reports/cancellation_report.csv): ")
        if not filename.endswith('.csv'):
            filename += '.csv'
        system.generate_cancellation_report(filename)

if __name__ == "__main__":
    main_menu()
