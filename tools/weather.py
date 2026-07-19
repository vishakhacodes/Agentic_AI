import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
WTTR_URL = "https://wttr.in"


def _open_meteo_weather(city: str):
    geo_response = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1},
        timeout=10,
    )
    geo_response.raise_for_status()
    geo_data = geo_response.json()

    results = geo_data.get("results")
    if not results:
        raise ValueError(f"City not found: {city}")

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
        f"Weather for {city_name}, {country}: {temperature} degrees C, "
        f"wind {windspeed} m/s, weather code {weather_code}. "
        f"Coordinates: {latitude}, {longitude}."
    )


def _wttr_weather(city: str):
    response = requests.get(
        f"{WTTR_URL}/{requests.utils.quote(city)}",
        params={"format": "j1"},
        timeout=15,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    data = response.json()

    current = data.get("current_condition", [{}])[0]
    if not current:
        raise ValueError("Weather data unavailable from wttr.in")

    temperature = current.get("temp_C")
    windspeed = current.get("windspeedKmph")
    description = current.get("weatherDesc", [{}])[0].get("value", "")

    return (
        f"Weather for {city}: {temperature} degrees C, wind {windspeed} km/h, {description}."
    )


def execute(arguments: dict):
    city = arguments.get("city")
    if not city:
        return "Weather error: city is required"

    try:
        return _open_meteo_weather(city)
    except Exception as exc:
        try:
            return _wttr_weather(city)
        except Exception as fallback_exc:
            return f"Weather error: primary provider failed ({exc}); fallback failed ({fallback_exc})"