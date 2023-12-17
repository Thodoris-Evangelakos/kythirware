"""
Module for managing bookings.

This module provides a class for representing a booking for a room.
It includes attributes for the booking ID, room name, arrival date, departure date, 
    and custom services.
The class also includes a method for retrieving the details of the booking.

Example usage:
    booking = Booking(1, "Room 101", "2022-01-01", "2022-01-05", "Breakfast")
    details = booking.get_booking_details()
    print(details)

Output:
    Booking ID: 1
    Room: Room 101
    Arrival: 2022-01-01
    Departure: 2022-01-05
    Custom Service: Breakfast
"""


class Booking:
    """
    Represents a booking for a room.

    Attributes:
        id (int): The unique identifier for the booking.
        room (str): The room name.
        arrival (str): The arrival date of the booking.
        departure (str): The departure date of the booking.
        custom_service (str): Any custom services requested for the booking.
    """

    def __init__(self, id, room, arrival, departure, custom_service):
        self.id = id
        self.room = room
        self.arrival = arrival
        self.departure = departure
        self.custom_service = custom_service

    def get_booking_details(self):
        """
        Returns the details of the booking.
        
        Returns:
            str: The details of the booking.
        """
        return f"Booking ID: {self.id}\nRoom: {self.room}\nArrival: {self.arrival}\nDeparture: {self.departure}\nCustom Service: {self.custom_service}"

