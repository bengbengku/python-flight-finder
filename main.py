from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch

flight_search = FlightSearch()

data_manager = DataManager()
data_sheet = data_manager.get_destination_data()

ORIGIN_CITY_IATA = "CGK"

if data_sheet[0]["iataCode"] == "":


    for row in data_sheet:
        row["iataCode"] = flight_search.get_destination_code(row['city'])

    data_manager.destination_data = data_sheet
    data_manager.update_destination_code()

tommorow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in data_sheet:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tommorow,
        to_time=six_months_from_today
    )











