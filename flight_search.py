import requests
from  flight_data import FlightData
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

kiwi_endpoint = "https://tequila-api.kiwi.com/"
KIWI_API_KEY = os.getenv("KIWI_KEY")


class FlightSearch:


    def get_destination_code(self, city_name):
        location_endpoint = f"{kiwi_endpoint}locations/query"

        query = {
            "term": city_name,
            "location_types": "city"
        }
        headers = {
            "apikey": KIWI_API_KEY
        }
        res = requests.get(url=location_endpoint, params=query, headers=headers)
        res.raise_for_status()
        data = res.json()["locations"]
        code = data[0]["code"]
        return code

    def check_flights(self, origin_code, destination_city_code, from_time, to_time):
        headers = {"apiKey": KIWI_API_KEY}
        query = {
            "fly_from": origin_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "IDR"
        }

        respons = requests.get(
            url=f"{kiwi_endpoint}v2/search",
            headers=headers,
            params=query
        )

        try:
            data = respons.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}")
            return None


        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )

        print(f"{flight_data.destination_city}: Rp. {flight_data.price}")

        return flight_data