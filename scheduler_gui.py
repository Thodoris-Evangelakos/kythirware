import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from hotel_manager import HotelManager
from hotel_manager import run_manager
from booking import Booking

Booking = Booking

class GUI:
    def __init__(self, root, manager):
        self.manager = manager
        self.root = root
        self.root.title("Hotel Manager")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.textbox = tk.Text(self.frame)
        self.textbox.pack()

        self.add_button = tk.Button(self.frame, text="Add booking", command=self.add_booking)
        self.add_button.pack(side="left")

        self.print_button = tk.Button(self.frame, text="Print today's jobs", command=self.print_todays_jobs)
        self.print_button.pack(side="left")

        self.load_button = tk.Button(self.frame, text="Load bookings from HTML", command=self.load_bookings_from_html)
        self.load_button.pack(side="left")

        self.print_and_output_button = tk.Button(self.frame, text="Print and physically output today's jobs", command=self.print_and_output_todays_jobs)
        self.print_and_output_button.pack(side="left")

        self.update_button = tk.Button(self.frame, text="Update custom service", command=self.update_custom_service)
        self.update_button.pack(side="left")

        self.dev_menu_button = tk.Button(self.frame, text="Developer Menu", command=self.dev_menu)
        self.dev_menu_button.pack(side="left")

    def add_booking(self):
        room = simpledialog.askstring("Add booking", "Enter room name:")
        arrival = simpledialog.askstring("Add booking", "Enter arrival date (DD/MM/YYYY):")
        departure = simpledialog.askstring("Add booking", "Enter departure date (DD/MM/YYYY):")
        custom_service = simpledialog.askstring("Add booking", "Enter custom service schedule (n for never, 1 for default, a number for custom days):")
        output = self.manager.add_booking(room, arrival, departure, custom_service)
        self.textbox.insert("end", output)

    def print_todays_jobs(self):
        output = self.manager.print_todays_jobs()
        self.textbox.insert("end", output)

    def load_bookings_from_html(self):
        file_path = filedialog.askopenfilename()
        self.manager.load_bookings_from_html(file_path)

    def print_and_output_todays_jobs(self):
        self.manager.print_todays_jobs(to_file=True)
        self.manager.print_file("jobs.txt")

    def update_custom_service(self):
        booking_id = simpledialog.askstring("Update custom service", "Enter booking ID:")
        new_custom_service = simpledialog.askstring("Update custom service", "Enter new custom service schedule (n for never, 1 for default, a number for custom days):")
        output = self.manager.update_custom_service(booking_id, new_custom_service)
        self.textbox.insert("end", output)

    def dev_menu(self):
        # Just an example, you can add more functionality here
        option = simpledialog.askstring("Developer Menu", "Enter option (1 - Print all bookings, 2 - Print jobs for the week):")
        if option == '1':
            output = self.manager.print_all_bookings()
            self.textbox.insert("end", output)
        elif option == '2':
            output = self.manager.print_week_jobs()
            self.textbox.insert("end", output)

def main():
    manager = run_manager()
    root = tk.Tk()
    gui = GUI(root, manager)
    root.mainloop()

if __name__ == "__main__":
    main()
