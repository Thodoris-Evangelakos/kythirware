"""
This module contains a class and a function to manage hotel bookings.

Classes:
    HotelManager: A class that provides methods to manage hotel bookings.

Functions:
    run_manager(): A function to initialize the HotelManager class with some predefined rooms and a save file.
"""

import datetime
import pickle
import os
import pandas as pd
import string
import win32api
import win32print
import json
from booking import Booking

SERVICES_FILE_PATH = "services.json"
RULES_FILE_PATH = "rules.json"

class HotelManager:

    """
    A class used to manage hotel bookings.

    ...

    Attributes
    ----------
    rooms : list
        a list of rooms available in the hotel
    bookings : list
        a list of all bookings made
    save_file : str
        the file path where the bookings are saved

    Methods
    -------
    load_bookings_from_html(file_path):
        Loads bookings from an HTML file and stores them in the bookings attribute.
    load_rules(file_path):
        Loads custom rules for bookings from a JSON file.
    update_custom_service(id, new_custom_service):
        Updates the custom service of a booking.
    save_bookings():
        Saves the current bookings to a pickle file.
    add_booking(room, arrival, departure, custom_service):
        Adds a new booking to the list of bookings.
    _get_padding(print_string):
        Internal method to get padding for print statements.
    print_todays_jobs(today=None, to_file=False):
        Prints the jobs for a specific day.
    print_file(file_path):
        Sends a file to the default printer.
    print_all_bookings():
        Prints all current bookings.
    print_week_jobs():
        Prints jobs for the entire week.
    """

    def __init__(self, rooms, save_file):
        
        """
        Initializes the HotelManager with a list of rooms and a save file.

        Parameters
        ----------
        rooms : list
            A list of rooms available in the hotel.
        save_file : str
            The file path where the bookings are saved.
        """

        self.rooms = rooms
        self.bookings = []
        self.save_file = save_file
        if os.path.exists(self.save_file):
            with open(self.save_file, "rb") as f:
                self.bookings = pickle.load(f)

    def load_bookings_from_html(self, file_path):

        """
        Loads bookings from an HTML file and stores them in the bookings list.
    
        Also loads custom services from a JSON file and updates them in the bookings list.
    
        Parameters
        ----------
        file_path : str
            The file path of the HTML file from where bookings are loaded.

        Returns
        -------
        str
            A message indicating whether the bookings and custom services were loaded successfully.
        """
    
        df = pd.read_html(file_path, skiprows=1)[0]
        headers = list(string.ascii_uppercase)[:24]
        df.columns = headers
        self.bookings = []
        rules = self.load_rules('rules.json')
        for _, row in df.iterrows():
            id = str(row['A'])  # get ID from column A
            room = str(row['G'])
            if id in rules:
                for arrival, departure in rules[id]:
                    custom_service = 1  # default custom_service, as it's not in the HTML file
                    self.bookings.append(Booking(id, room, arrival, departure, custom_service))
            else:
                arrival = datetime.datetime.strptime(row['C'], "%d/%m/%Y").date()
                departure = datetime.datetime.strptime(row['D'], "%d/%m/%Y").date()
                custom_service = 1  # default custom_service, as it's not in the HTML file
                self.bookings.append(Booking(id, room, arrival, departure, custom_service))
    
        # Load custom services
        self.load_custom_services(SERVICES_FILE_PATH)
    
        self.save_bookings()
        return "Bookings and custom services loaded successfully from HTML and JSON."

    def load_rules(self, file_path):

        """
        Loads custom rules for bookings from a JSON file.

        Parameters
        ----------
        file_path : str
            The file path of the JSON file from where rules are loaded.

        Returns
        -------
        dict
            A dictionary containing the rules for the bookings.
        """

        with open(file_path, 'r') as f:
            rules = json.load(f)
        return {key: [(datetime.datetime.strptime(stay[0], "%d/%m/%Y").date(), 
                       datetime.datetime.strptime(stay[1], "%d/%m/%Y").date()) 
                      for stay in stays] 
                for key, stays in rules.items()}

    def load_custom_services(self, file_path):

        """
        Loads custom services for bookings from a JSON file.
    
            The services file should be formatted as a dictionary where each key is a booking ID
            and each value is the custom service for the booking.
    
            Parameters
            ----------
            file_path : str
                The file path of the JSON file from where custom services are loaded.
    
            Returns
            -------
            str
                A message indicating whether the custom services were loaded successfully.
            """
    
        with open(file_path, 'r') as f:
            custom_services = json.load(f)

        for booking in self.bookings:
            if booking.id in custom_services:
                booking.custom_service = custom_services[booking.id]
    
        return "Custom services loaded successfully from JSON."

    def update_custom_service(self, id, new_custom_service):
        
        """
        Updates the custom service of a booking with a given ID.

        Parameters
        ----------
        id : str
            The ID of the booking.
        new_custom_service : int
            The new custom service value.

        Returns
        -------
        str
            A message indicating whether the custom service was updated successfully.
        """

        for booking in self.bookings:
            if booking.id == id:
                booking.custom_service = new_custom_service
                self.save_bookings()
                return f"Custom service for booking {id} updated successfully"
        return f"No booking found with ID {id}"

    def save_bookings(self):

        """
        Saves the current bookings to a pickle file.
        """

        with open(self.save_file, "wb") as f:
            pickle.dump(self.bookings, f)

    def add_booking(self, room, arrival, departure, custom_service):

        """
        Adds a new booking to the list of bookings.

        Parameters
        ----------
        room : str
            The room for the booking.
        arrival : str
            The arrival date for the booking in the format "dd/mm/yyyy".
        departure : str
            The departure date for the booking in the format "dd/mm/yyyy".
        custom_service : str
            The custom service for the booking.

        Returns
        -------
        str
            A message indicating whether the booking was added successfully.
        """

        room = room.upper()
        if room not in self.rooms:
            return "Invalid room name"

        arrival = datetime.datetime.strptime(arrival, "%d/%m/%Y").date()
        departure = datetime.datetime.strptime(departure, "%d/%m/%Y").date()
        if departure <= arrival:
            return "Departure date must be after arrival date"

        for booking in self.bookings:
            if booking.room == room and not (arrival >= booking.departure or departure <= booking.arrival):
                return "This room is already occupied during the given period"

        if custom_service.lower() != 'n':
            custom_service = int(custom_service) if custom_service.isdigit() else 1

        self.bookings.append(Booking(12345, room, arrival, departure, custom_service))
        self.save_bookings()
        return "Booking added successfully\n"

    def _get_padding(self, print_string : str) -> str:

        """
        Gets the padding for a string to be printed.

        This is an internal method used to format strings for printing.

        Parameters
        ----------
        print_string : str
            The string for which the padding is to be calculated.

        Returns
        -------
        str
            A string of spaces that serves as padding for `print_string`, followed by an asterisk.
        """

        return ((30 - len(print_string) - 1))*' '+'*'

    def print_todays_jobs(self, today=None, to_file=False):
        """
        Prints the jobs for a specific day.
    
        Parameters
        ----------
        today : datetime.date, optional
            The date for which the jobs are to be printed. Defaults to the current date if not provided.
        to_file : bool, optional
            Whether to print the jobs to a file. Defaults to False.
    
        Returns
        -------
        str
            A string representing the jobs for the specified day.
        """
    
        if today is None:
            today = datetime.date.today()
    
        if to_file:
            file = open('jobs.txt', 'w')
        else:
            file = None
    
        job_list = []
        unique_jobs = set()
        print_string = f"{'*' * 10}{today.strftime('%d/%m/%Y')}{'*' * 10}"
        print(print_string, file=file)
        job_list.append(print_string)
        for booking in self.bookings:
            if booking.arrival <= today <= booking.departure:
                days = (today - booking.arrival).days
                if booking.custom_service == 'n':
                    continue
                elif today == booking.arrival:
                    print_string = f"* {booking.room}: Γενικό"
                elif today == booking.departure:
                    print_string = f"* {booking.room}: Check-out"
                elif days % (2 * int(booking.custom_service)) == int(booking.custom_service):
                    print_string = f"* {booking.room}: Πετσέτες"
                elif days % (2 * int(booking.custom_service)) == 0 and days != 0:
                    print_string = f"* {booking.room}: Πετσέτες/Σεντόνια"
                else:
                    continue
    
                unique_jobs.add(print_string)

        """for booking in self.bookings:
            if booking.arrival <= today <= booking.departure:
                days = (today - booking.arrival).days
                if booking.custom_service == 'n':
                    continue
                else:
                    if today == booking.arrival:
                         print_string = f"* {booking.room}: Γενικό"""

    
    
        for job in unique_jobs:
            job_list.append(job + self._get_padding(job))
            print(job + self._get_padding(job), file=file)
    
        job_list.append('*'*30)
        print('*'*30, file=file)
    
        return '\n'.join(job_list)



    def print_file(self, file_path):

        """
        Sends a file to the default printer.

        Parameters
        ----------
        file_path : str
            The file path of the file to be printed.
        """

        win32api.ShellExecute(
            0,
            "print",
            file_path,
            '/d:"%s"' % win32print.GetDefaultPrinter(),
            ".",
            0
        )

    def print_all_bookings(self):

        """
        Prints all current bookings.

        Returns
        -------
        str
            A string representing all the current bookings.
        """

        booking_list = ["All current bookings:"]
        for booking in self.bookings:
            booking_list.append(f"Room: {booking.room}, Arrival: {booking.arrival}, Departure: {booking.departure}, Custom service: {booking.custom_service}")
        return '\n'.join(booking_list)

    def print_week_jobs(self):

        """
        Prints jobs for the entire week starting from today.

        Returns
        -------
        str
            A string representing the jobs for the week.
        """

        job_list = []
        today = datetime.date.today()
        for i in range(7):
            day = today + datetime.timedelta(days=i)
            job_list.append(self.print_todays_jobs(day))
        return '\n'.join(job_list)



def run_manager():

    """
    Initializes the `HotelManager` class with predefined rooms and a save file.

    Returns
    -------
    HotelManager
        An instance of the `HotelManager` class.
    """

    rooms = [f"R{num}" for num in [11, 12, 13, 14, 15, 16, 21, 22, 23, 24, 31, 32, 33, 34]]
    return HotelManager(rooms, "bookings.pkl")
