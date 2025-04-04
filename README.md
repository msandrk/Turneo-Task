## Booking cost currency converter API
A simple API that can be used to convert the prices of bookings fetched from Turneo API into the desired currency. Conversion is done with the exchange rate that was in effect on the day the booking was made. If it's not possible to retrieve data from that day, latest exchange rates are used instead.

### API Documentation
This simple API has only one endpoint: `/api/v1/currency-converter`. This endpoint requires two query parameters:
1. `date` - A date in ISO 8601 format for which the bookings that were made will be retrieved.
2. `currency` - An three-letter ISO 4217 code of desired currency for the booking prices.

The API returns the following attributes:
* `bookingCode` - short code that designates this booking
* `experienceName` - name of the experience booked
* `rateName` - name of the rate used
* `numberOfParticipants` - total number of people for which the booking was made
* `originalPrice` - price in the original currency 
* `convertedPrice` - price in requested currency

### API Setup
Easiest way to setup the API is to build a [Docker](https://www.docker.com/) image from the `Dockerfile` present in this repo. After cloning the repository, please make sure to create and fill out a `.env` file with the keys present in `.env.example` file in this repository and corresponding values. Although usually highly discouraged, I have decided to share the API key for a exchange rates API with you directly through `.env.example` in this repository so you don't have to register for this API yourselves.

To do so run:
```bash
# presuming you have Docker installed
$ git clone git@github.com:msandrk/Turneo-Task.git
$ cd Turneo-Task
$ docker build -t booking-currency-converter .
$ docker run --rm -d --name booking-currency-converter-api -p 8000:8000 booking-currency-converter
```

After building the Docker image and running a container from you can send a request to the http://localhost:8000/api/v1/currency-converter with `date` and `currency` query parameters specified.
