import datetime
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

from .models import ConvertedCurrencyBooking


def request_bookings_data(params: dict[str, str]) -> requests.Response:
    bookings_URL = f"{os.environ['TURNEO_API']}/bookings"
    bookings_headers = {"x-api-key": os.environ["TURNEO_API_KEY"]}

    return requests.get(bookings_URL, params=params, headers=bookings_headers)


def prune_booking_data(bookings: list[dict[str, Any]]) -> list[ConvertedCurrencyBooking]:
    return [
        ConvertedCurrencyBooking(
            bookingCode=b["bookingCode"],
            experienceName=b["experience"]["name"],
            rateName=b["rateName"],
            numberOfParticipants=calculate_number_of_participants(b),
            originalPrice={**b["finalPrice"]},
        )
        for b in bookings
    ]


def calculate_number_of_participants(booking: dict[str, Any]) -> int:
    return sum([rate["quantity"] for rate in booking["ratesQuantity"]])


def is_valid_target_currency(currency: str):
    available_currencies = _fetch_available_currencies()

    return currency in available_currencies


def _fetch_available_currencies():
    response = requests.get(f"{os.environ['EXCHANGE_RATE_API_ENDPOINT']}/currencies.json")

    if response.status_code != 200:
        return []

    return response.json().keys()


def request_exchange_rates_data(date: datetime.date) -> requests.Response:
    iso_date = date.isoformat()

    query_params = {"app_id": os.environ["EXCHANGE_RATE_API_KEY"]}
    response = requests.get(f"{os.environ['EXCHANGE_RATE_API_ENDPOINT']}/{iso_date}.json", params=query_params)

    if response.status_code == 200:
        return response

    return requests.get(f"{os.environ['EXCHANGE_RATE_API_ENDPOINT']}/latest.json", params=query_params)


def convert_currency_data(
    booking_data: list[ConvertedCurrencyBooking], exchange_rates: dict[str, float], target_currency: str
) -> None:
    target_currency = target_currency.upper()

    for booking in booking_data:
        (original_price, original_currency) = booking.originalPrice.values()

        # since changing the base currency is not possible in the free tier for this
        # API, we do it ourselves which probably means a bit less precise conversion.
        convertedPrice = original_price * (1 / exchange_rates[original_currency]) * exchange_rates[target_currency]

        booking.convertedPrice = {"amount": round(convertedPrice, 2), "currency": target_currency.upper()}
