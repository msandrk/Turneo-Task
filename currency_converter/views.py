import datetime
import urllib
import urllib.parse
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET

from . import utils


@require_GET
def index(request: HttpRequest) -> JsonResponse:

    target_date = request.GET.get("date")
    target_currency = request.GET.get("currency")

    if not target_date or not target_currency:

        missing_param = "date" if not target_date else "currency"

        return JsonResponse(
            data={"data": [], "message": f"Missing mandatory query parameter '{missing_param}'."}, status=400
        )

    try:
        target_date = datetime.date.fromisoformat(target_date)
        end_date = target_date + datetime.timedelta(days=1)
    except ValueError as e:
        return JsonResponse({"data": [], "message": str(e)}, status=400)

    query_params = {"bookingCreated[gte]": target_date.isoformat(), "bookingCreated[lt]": end_date.isoformat()}

    bookings_res = utils.fetch_bookings_data(query_params)

    if bookings_res.status_code != 200:
        return JsonResponse(data={"data": [], "message": "Failed to fetch data about bookings"}, status=400)

    body = bookings_res.json()

    booking_data = [*body["results"]]

    # this won't scale well for big number of pages
    # maybe also add pagination
    while body["next"]:
        next_page_url = urllib.parse.unquote(body["next"])
        query_params = urllib.parse.parse_qs(next_page_url)

        bookings_res = utils.fetch_bookings_data(query_params)
        if bookings_res.status_code != 200:
            return JsonResponse(data={"data": [], "message": "Failed to fetch data about bookings"}, status=400)

        booking_data.extend(body["results"])

    pruned_booking_data = utils.prune_booking_data(booking_data)

    return JsonResponse(data={"size": len(pruned_booking_data), "data": pruned_booking_data, "message": "OK"})
