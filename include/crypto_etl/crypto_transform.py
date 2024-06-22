from typing import Optional
import pendulum


def crypto_transform(response: Optional[dict]) -> Optional[dict]:
    """Transforms Crypto Polygon API response.

    The available transformations are:
        - filters relevant information
            - symbol
            - day
            - open
            - close
        - transforms to dict with the following keys
            - crypto_symbol
            - date_capture
            - price_currency
            - price_open
            - price_close

    Args:
        response:
            Crypto Polygon API response.
        
    Returns:
        Tranformed Crypto Polygon API data, otherwise None.

        {
            'crypto_symbol': 'BTC',
            'price_currency': 'USD',
            'date_capture': "2023-01-01",
            'price_open': 16532,
            'price_close': 16611.58,
        }
    """
    if response is None:
        return None
    
    # Polygon API: "symbol": "BTC-USD"
    crypto_symbol, price_currency = response["symbol"].split("-")
    # Polygon API: "day": "2023-01-01T00:00:00Z"
    date_capture = pendulum.parse(response["day"]).to_date_string()
    # Polygon API: "open": 16532
    price_open = response["open"]
    # Polygon API: "close": 16611.58
    price_close = response["close"]

    return {
        "crypto_symbol": crypto_symbol,
        "price_currency": price_currency,
        "date_capture": date_capture,
        "price_open": price_open,
        "price_close": price_close,
    }
