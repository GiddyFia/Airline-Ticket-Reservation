import csv
import random
from datetime import datetime

# Initialize global variables for seats and file path
MAX_SEATS = 100
CSV_FILE = 'booking_records.csv'


# Load existing records from CSV
def load_records():
    records = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            records = list(reader)
    except FileNotFoundError:
        print("Booking record file not found, starting fresh.")
    return records


# Save records to CSV
def save_records(records):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['customer_id', 'ticket_number', 'seat_number', 'booking_time',
                                                  'cancellation_time'])
        writer.writeheader()
        writer.writerows(records)


# Generate unique customer ID and ticket number
def generate_ticket_number():
    customer_id = random.randint(100, 999)
    ticket_number = f"{customer_id}-{random.randint(10000, 99999)}"
    return customer_id, ticket_number


# Display remaining seats
def display_available_seats(records):
    booked_seats = {int(record['seat_number']) for record in records if record['cancellation_time'] == ''}
    available_seats = MAX_SEATS - len(booked_seats)
    print(f"{available_seats} seats available")


# Book a ticket
def book_ticket(records):
    customer_id, ticket_number = generate_ticket_number()
    booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    available_seats = [seat for seat in range(1, MAX_SEATS + 1) if
                       not any(record['seat_number'] == str(seat) for record in records)]

    if available_seats:
        seat_number = available_seats[0]  # Assign the first available seat
        records.append({
            'customer_id': str(customer_id),
            'ticket_number': ticket_number,
            'seat_number': str(seat_number),
            'booking_time': booking_time,
            'cancellation_time': ''
        })
        print(f"Ticket booked! Ticket number: {ticket_number}, Seat number: {seat_number}")
    else:
        print("No available seats.")


# Cancel a ticket
def cancel_ticket(records):
    ticket_number = input("Enter ticket number to cancel: ")
    for record in records:
        if record['ticket_number'] == ticket_number and record['cancellation_time'] == '':
            record['cancellation_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Ticket canceled.")
            return
    print("Ticket not found or already canceled.")


# Query ticket info
def view_ticket_info(records):
    ticket_number = input("Enter ticket number to view information: ")
    for record in records:
        if record['ticket_number'] == ticket_number:
            print(record)
            return
    print("Ticket not found.")


# Main menu
def main():
    records = load_records()
    while True:
        print(
            "\nMenu:\n1. Book a ticket\n2. Cancel a ticket\n3. View available seats\n4. View ticket information\n5. Quit")
        choice = input("Choose an option: ")
        if choice == '1':
            book_ticket(records)
        elif choice == '2':
            cancel_ticket(records)
        elif choice == '3':
            display_available_seats(records)
        elif choice == '4':
            view_ticket_info(records)
        elif choice == '5':
            save_records(records)
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
