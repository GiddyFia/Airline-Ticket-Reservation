import tkinter as tk
from tkinter import messagebox
import sqlite3

def submit_review(flight_id, user_id, review_text, rating):
    conn = sqlite3.connect('airline_reservation.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (flight_id, user_id, review_text, rating) VALUES (?, ?, ?, ?)",
                   (flight_id, user_id, review_text, rating))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Review submitted successfully!")

# Example GUI for submitting a review
def review_gui():
    window = tk.Tk()
    window.title("Submit Review")

    tk.Label(window, text="Flight ID:").grid(row=0)
    tk.Label(window, text="User  ID:").grid(row=1)
    tk.Label(window, text="Review:").grid(row=2)
    tk.Label(window, text="Rating (1-5):").grid(row=3)

    flight_id_entry = tk.Entry(window)
    user_id_entry = tk.Entry(window)
    review_entry = tk.Entry(window)
    rating_entry = tk.Entry(window)

    flight_id_entry.grid(row=0, column=1)
    user_id_entry.grid(row=1, column=1)
    review_entry.grid(row=2, column=1)
    rating_entry.grid(row=3, column=1)

    tk.Button(window, text="Submit", command=lambda: submit_review(flight_id_entry.get(), user_id_entry.get(), review_entry.get(), rating_entry.get())).grid(row=4, column=1)

    window.mainloop()

review_gui()