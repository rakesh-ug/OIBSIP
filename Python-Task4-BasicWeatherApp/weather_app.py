"""OIBSIP Python Task 4: current weather from OpenWeatherMap."""

import math
from pathlib import Path

import requests

API_URL = "https://api.openweathermap.org/data/2.5/weather"
ENV_PATH = Path(__file__).resolve().parent / ".env"


class WeatherError(Exception):
    """User-readable weather lookup or configuration error."""


def read_api_key(path: Path = ENV_PATH) -> str:
    """Read OPENWEATHER_API_KEY from a local .env file (never from source code)."""
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except FileNotFoundError as exc:
        raise WeatherError("Missing .env file. Copy .env.example to .env and add your API key.") from exc
    except OSError as exc:
        raise WeatherError("Cannot read .env; check file permissions.") from exc
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        if name.strip() == "OPENWEATHER_API_KEY":
            value = value.strip().strip('"\'').strip()
            if value and value != "your_api_key_here":
                return value
            break
    raise WeatherError("Set OPENWEATHER_API_KEY in .env to your real OpenWeatherMap key.")


def _number(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise WeatherError(f"Weather service returned an invalid {field} value.")
    return float(value)


def get_weather(city: str, api_key: str, session=None) -> dict:
    """Fetch current weather; optional session lets tests avoid real network calls."""
    city = city.strip()
    if not city or len(city) > 100:
        raise WeatherError("Enter a city name (1 to 100 characters).")
    if not api_key.strip():
        raise WeatherError("Configure your API key in .env first.")
    client = session if session is not None else requests
    try:
        response = client.get(API_URL, params={"q": city, "appid": api_key, "units": "metric"}, timeout=10)
    except requests.Timeout as exc:
        raise WeatherError("Request timed out. Check your connection and try again.") from exc
    except requests.RequestException as exc:
        raise WeatherError("Network error. Check your connection and try again.") from exc
    if response.status_code == 404:
        raise WeatherError("City not found. Try a city name with a country code, e.g., Paris,FR.")
    if response.status_code == 401:
        raise WeatherError("API key rejected. Check the key in .env; new keys may take time to activate.")
    if response.status_code == 429:
        raise WeatherError("API rate limit reached. Wait a little and retry.")
    if response.status_code != 200:
        raise WeatherError(f"Weather service error (HTTP {response.status_code}). Try again later.")
    try:
        data = response.json()
        main, wind = data["main"], data["wind"]
        description = data["weather"][0]["description"]
        name = data["name"]
        country = data.get("sys", {}).get("country", "")
        temp_c = _number(main["temp"], "temperature")
        feels_c = _number(main["feels_like"], "feels-like temperature")
        humidity = _number(main["humidity"], "humidity")
        wind_ms = _number(wind["speed"], "wind speed")
        if not 0 <= humidity <= 100 or wind_ms < 0:
            raise WeatherError("Weather service returned out-of-range humidity or wind speed.")
        if not isinstance(description, str) or not isinstance(name, str) or not name:
            raise WeatherError("Weather service returned incomplete location details.")
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise WeatherError("Weather service returned incomplete or malformed data.") from exc
    return {"city": name, "country": country, "description": description,
            "temp_c": temp_c, "temp_f": temp_c * 9 / 5 + 32,
            "feels_c": feels_c, "humidity": humidity, "wind_ms": wind_ms,
            "wind_kmh": wind_ms * 3.6}


def main() -> None:
    print("\n=== CURRENT WEATHER ===")
    try:
        key = read_api_key()
    except WeatherError as exc:
        print(f"Error: {exc}")
        return
    while True:
        try:
            city = input("City (or q to quit): ").strip()
            if city.lower() == "q":
                print("Goodbye!")
                return
            report = get_weather(city, key)
        except WeatherError as exc:
            print(f"Error: {exc}\n")
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
        location = report["city"] + (f", {report['country']}" if report["country"] else "")
        print(f"\n{location} | {report['description'].capitalize()}")
        print(f"Temperature: {report['temp_c']:.1f} °C / {report['temp_f']:.1f} °F")
        print(f"Feels like:  {report['feels_c']:.1f} °C")
        print(f"Humidity:    {report['humidity']:.0f}%")
        print(f"Wind speed:  {report['wind_ms']:.1f} m/s ({report['wind_kmh']:.1f} km/h)\n")


if __name__ == "__main__":
    main()
