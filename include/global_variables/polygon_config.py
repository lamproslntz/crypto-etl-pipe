from pendulum import datetime
from decouple import config


default_args = {
    "api_key": config("POLYGON_API_KEY"),
    "base_url": "https://api.polygon.io/v2/aggs/ticker/",
    "cryptoTicker": "X:BTCUSD",
    "multiplier": "1",
    "from": "2023-01-01",
    "to": "2023-02-01",
    "adjusted": "true",
    "sort": "asc",
}
