import dataclasses


@dataclasses.dataclass
class ConvertedCurrencyBooking:
    bookingCode: str
    experienceName: str
    rateName: str
    numberOfParticipants: str
    originalPrice: dict[str, float | str]
    convertedPrice: dict[str, float | str] = None
