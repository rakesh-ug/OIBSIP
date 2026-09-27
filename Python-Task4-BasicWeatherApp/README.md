# Basic Weather App

A Python command-line weather app that fetches current conditions for a city using OpenWeatherMap.

## What it does

- Accepts a city name, optionally with a country code such as `Paris,FR`.
- Displays the condition, temperature in Celsius and Fahrenheit, humidity, and wind speed.
- Handles empty input, unknown cities, invalid API keys, timeouts, and service errors without crashing.
- Lets you search again or enter `q` to quit.

## Setup and run

Requires Python 3.9 or newer, an internet connection, and your own OpenWeatherMap API key.

```bash
python3 -m pip install -r requirements.txt
```

Create a `.env` file beside `weather_app.py` by copying `.env.example`, then replace `your_api_key_here` with your own key. For example:

```text
OPENWEATHER_API_KEY=your_actual_key
```

Get a key from https://openweathermap.org/api. New keys can take time to activate. The `.env` file is ignored by Git and must not be uploaded.

```bash
python3 weather_app.py
```

Try `London` to see live conditions; the numbers change with the weather. Use `python3` to run this project.

## Test

```bash
python3 -m unittest discover -v
```

The tests simulate responses, so they work without an API key or live weather connection.
