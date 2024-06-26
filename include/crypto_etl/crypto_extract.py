import logging
from typing import Optional

import requests

logger = logging.getLogger(__package__)


def crypto_extract(
    crypto_symbol: str, capture_date: str, polygon_api_key: str
) -> Optional[dict]:
    """Extracts open and close prices of a crypto symbol on a certain day using Crypto Polygon API.

    Args:
        crypto_symbol:
            Crypto symbol (e.g. BTC, DOGE, etc.).
        capture_date:
            Date (YYYY-MM-DD) of request.
        polygon_api_key:
            Polygon API key.

    Returns:
        Open and close prices of a crypto symbol on a certain day, otherwise None.
        See Crypto Polygon API documentation [here](https://polygon.io/docs/crypto/getting-started).
    """
    crypto_symbol = crypto_symbol.upper()

    response = None
    try:
        response_request = requests.get(
            f"https://api.polygon.io/v1/open-close/crypto/{crypto_symbol}/USD/"
            f"{capture_date}?adjusted=true&apiKey={polygon_api_key}"
        )
        response_request.raise_for_status()

        response = response_request.json()
    except requests.exceptions.HTTPError:
        logger.error(response_request.json())

    return response
