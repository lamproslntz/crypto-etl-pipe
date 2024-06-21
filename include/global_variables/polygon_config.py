from decouple import config

default_args = {
    "api_key": config("POLYGON_API_KEY"),
    "base_url": "https://api.polygon.io/v1/open-close/crypto",
    "symbol_from": "BTC",
    "symbol_to": "USD",
    "date_capture": "2023-01-01",
    "price_adjusted": "true",
}
