import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def execute(arguments: dict):
    city = arguments.get("city")
    if not city:
        return "Weather error: city is required"

    try:
        geo_response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1},
            timeout=10,
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        results = geo_data.get("results")
        if not results:
            return f"City not found: {city}"

        location = results[0]
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        city_name = location.get("name", city)
        country = location.get("country", "")

        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True,
                "timezone": "auto",
            },
            timeout=10,
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data.get("current_weather") or {}
        temperature = current.get("temperature")
        windspeed = current.get("windspeed")
        weather_code = current.get("weathercode")

        return (
            f"Weather for {city_name}, {country}: {temperature}°C, "
            f"wind {windspeed} m/s, weather code {weather_code}. "
            f"Coordinates: {latitude}, {longitude}."
        )
    except requests.RequestException as exc:
        return f"Weather error: {exc}"

        