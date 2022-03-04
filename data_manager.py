import requests
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from pprint import pprint

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/80f334f234ee9a1e4287c90ce17786c5/flightDealsExercise/prices"
AUTH_SHEETY_BEARER = os.getenv("BEARER")

sheet_headers = {
    "Authorization": AUTH_SHEETY_BEARER
}


class DataManager:
    def __init__(self):
        self.destination_data = {}


    def get_destination_data(self):
        sheety_res = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=sheet_headers)
        sheety_res.raise_for_status()
        data = sheety_res.json()["prices"]
        self.destination_data = data

        return self.destination_data

    def update_destination_code(self):
        for city in self.destination_data:
            sheety_update = {
                "price":
                    {
                        "iataCode": city["iataCode"]
                    }
            }

            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=sheety_update,
                headers=sheet_headers
            )
            print(response.text)

