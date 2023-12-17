# Kythirware Hotel Management System

This is a hotel management system developed in Python. It provides functionalities like managing bookings, printing jobs, and handling custom services.

## Features

- Load bookings from an HTML file (Managinng.com provides a .xls file but in reality it's an HTML file)
- Load custom rules for bookings from a JSON file
- Update the custom service of a booking
- Save the current bookings to a pickle file
- Add a new booking to the list of bookings
- Print jobs for a specific day
- Print all current bookings
- Print jobs for the entire week

## Usage

The main classes in this project are `HotelManager` in [hotel_manager.py](hotel_manager.py) and `GUI` in [scheduler_gui.py](scheduler_gui.py).
To use the program simply run `python3 scheduler_gui.py`. Make sure that the aforemetioned .xls file is in the program's root directory

### HotelManager

The `HotelManager` class is used to manage hotel bookings. It has methods like [`load_custom_services`](hotel_manager.py), [`update_custom_service`](hotel_manager.py), and [`print_todays_jobs`](hotel_manager.py).

### GUI

The `GUI` class provides a graphical user interface for the Hotel Manager application. It has methods like [`print_todays_jobs`](scheduler_gui.py) and [`dev_menu`](scheduler_gui.py).

## Installation

run `pip install requiremements.txt`

## Contributing

WIP

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License. See the [LICENSE](LICENSE) file for details.