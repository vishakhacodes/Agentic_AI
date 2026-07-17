import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def execute(arguments: dict):
    location = (
        arguments.get("location")
        or arguments.get("address")
        or arguments.get("query")
    )

    if not location:
        return "Geocoding error: missing location or address"

    try:
        response = requests.get(
            GEOCODING_URL,
            params={"name": location, "count": 1},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return f"Location not found: {location}"

        place = data["results"][0]
        name = place.get("name", "Unknown location")
        country = place.get("country", "")
        latitude = place.get("latitude")
        longitude = place.get("longitude")
        timezone = place.get("timezone", "")

        return (
            f"{name}, {country} | Latitude: {latitude} | Longitude: {longitude}"
            + (f" | Timezone: {timezone}" if timezone else "")
        )
    except requests.RequestException as exc:
        return f"Geocoding error: {exc}"
