import logging
from typing import Optional

import requests

logger = logging.getLogger(__package__)


def crypto_extract(polygon_api_key: str) -> Optional[dict]:
    """Extracts open and close prices of a crypto symbol on a certain day using Crypto Polygon API.

    Args:
        polygon_api_key:
            Polygon API key.

    Returns:
        Open and close prices of a crypto symbol on a certain day, otherwise None.
        See Crypto Polygon API documentation [here](https://polygon.io/docs/crypto/getting-started).
    """
    response = None
    try:
        response_request = requests.get(
            f"https://api.polygon.io/v1/open-close/crypto/BTC/USD/2023-01-01?adjusted=true&apiKey={polygon_api_key}"
        )
        response_request.raise_for_status()

        response = response_request.json()
    except requests.exceptions.HTTPError:
        logger.error(response_request.json())

    return response
