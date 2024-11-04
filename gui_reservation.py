import tkinter as tk
from tkinter import messagebox
import csv
import random


# Load and save functions for reading/writing ticket data
def load_records(filename="booking_records.csv"):
    records = []
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            records = list(reader)
    except FileNotFoundError:
        pass
    return records


def save_records(records, filename="booking_records.csv"):
    with open(filename, mode='w', newline='') as file:
        fieldnames = ["customer_id", "ticket_number", "seat_number"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


# Generate unique ticket number
def generate_ticket_number(customer_id):
    return f"{customer_id}-{random.randint(10000, 99999)}"


class AirlineReservationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Airline Ticket Reservation")
        self.records = load_records()
        self.seats = {str(i): None for i in range(1, 101)}  # 100 seats available
        self.update_seat_count()

        # Label and Entry Widgets
        self.ticket_label = tk.Label(root, text="Ticket Number:")
        self.ticket_label.pack()
        self.ticket_entry = tk.Entry(root)
        self.ticket_entry.pack()

        self.seats_label = tk.Label(root, text=f"Available Seats: {self.count_available_seats()}")
        self.seats_label.pack()

        # Buttons
        self.book_button = tk.Button(root, text="Book Ticket", command=self.book_ticket)
        self.book_button.pack()

        self.cancel_button = tk.Button(root, text="Cancel Ticket", command=self.cancel_ticket)
        self.cancel_button.pack()

        self.update_button = tk.Button(root, text="Update Booking", command=self.update_booking)
        self.update_button.pack()

        self.quit_button = tk.Button(root, text="Quit", command=self.quit_program)
        self.quit_button.pack()

    # Function to count available seats
    def count_available_seats(self):
        return sum(1 for seat in self.seats.values() if seat is None)

    def update_seat_count(self):
        self.seats_label.config(text=f"Available Seats: {self.count_available_seats()}")

    # Book ticket function
    def book_ticket(self):
        if self.count_available_seats() <= 0:
            messagebox.showinfo("Error", "No seats available.")
            return

        customer_id = str(random.randint(100, 999))
        ticket_number = generate_ticket_number(customer_id)
        for seat_number, occupant in self.seats.items():
            if occupant is None:
                self.seats[seat_number] = ticket_number
                self.records.append(
                    {"customer_id": customer_id, "ticket_number": ticket_number, "seat_number": seat_number})
                save_records(self.records)
                self.update_seat_count()
                messagebox.showinfo("Booking Success", f"Ticket {ticket_number} booked for Seat {seat_number}")
                return

    # Cancel ticket function
    def cancel_ticket(self):
        ticket_number = self.ticket_entry.get()
        if not ticket_number:
            messagebox.showerror("Error", "Please enter a valid ticket number.")
            return

        for record in self.records:
            if record["ticket_number"] == ticket_number:
                seat_number = record["seat_number"]
                self.records.remove(record)
                self.seats[seat_number] = None
                save_records(self.records)
                self.update_seat_count()
                messagebox.showinfo("Cancellation Success",
                                    f"Ticket {ticket_number} for Seat {seat_number} has been canceled.")
                return
        messagebox.showerror("Error", "Ticket number not found.")

    # Update booking function
    def update_booking(self):
        ticket_number = self.ticket_entry.get()
        if not ticket_number:
            messagebox.showerror("Error", "Please enter a valid ticket number.")
            return

        for record in self.records:
            if record["ticket_number"] == ticket_number:
                # Perform update logic (e.g., change seat)
                messagebox.showinfo("Update Success", f"Booking for Ticket {ticket_number} updated.")
                save_records(self.records)
                return
        messagebox.showerror("Error", "Ticket number not found.")

    # Quit program function
    def quit_program(self):
        save_records(self.records)
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = AirlineReservationGUI(root)
    root.mainloop()
