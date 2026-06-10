# Tour & Travel Management System

A comprehensive management system for handling tour and travel operations, including customer management, tour packages, bookings, hotel reservations, transportation, payments, schedules, and report generation.

## Features

- **Customer Management**: Register and view customer details and booking history.
- **Tour Package Management**: Create and view available tour packages.
- **Booking Management**: Create and cancel bookings, and track check-in/check-out status.
- **Hotel Reservation Management**: Manage hotels and their available rooms.
- **Transportation Management**: Add and search for various transport modes (Bus, Flight, Train, Cab).
- **Payment Management**: Process payments for bookings.
- **Travel Schedule Management**: Manage travel itineraries and schedules.
- **Report Generation**: Generate CSV reports for bookings, revenue, customers, package popularity, and cancellations.
- **Dual Interface**: Supports both a Command Line Interface (CLI) and a Graphical User Interface (GUI).

## Installation

Ensure you have Python installed. You may need to install the following dependency:

```bash
pip install customtkinter
```

## Usage

### Command Line Interface (CLI)
To run the system via the terminal:
```bash
python main.py
```

### Graphical User Interface (GUI)
To run the system with a modern graphical interface:
```bash
python gui_app.py
```

## Project Structure

- `core/`: Contains the core logic and management classes.
- `models/`: Defines the data models for various entities.
- `utils/`: Contains utility functions and helpers.
- `data/`: Stores persistent data (if applicable).
- `main.py`: Entry point for the CLI application.
- `gui_app.py`: Entry point for the GUI application.
