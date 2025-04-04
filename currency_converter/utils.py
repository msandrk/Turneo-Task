import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


def fetch_bookings_data(params: dict[str, str]) -> requests.Response:
    bookings_URL = f"{os.environ['TURNEO_API']}/bookings"
    bookings_headers = {"x-api-key": os.environ["TURNEO_API_KEY"]}

    return requests.get(bookings_URL, params=params, headers=bookings_headers)


def prune_booking_data(bookings: list[dict[str, Any]]) -> list[dict[str, str | int]]:
    return [
        {
            "bookingCode": b["bookingCode"],
            "experienceName": b["experience"]["name"],
            "rateName": b["rateName"],
            "numberOfParticipants": calculate_number_of_participants(b),
            "totalPrice": {**b["finalPrice"]},
        }
        for b in bookings
    ]


def calculate_number_of_participants(booking: dict[str, Any]) -> int:
    return sum([rate["quantity"] for rate in booking["ratesQuantity"]])
