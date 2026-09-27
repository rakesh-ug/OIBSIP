"""Mocked tests: no API key or live network required."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
import requests
from weather_app import WeatherError, get_weather, read_api_key


class TestWeather(unittest.TestCase):
    def setUp(self):
        self.session = Mock()
        self.response = Mock(status_code=200)
        self.response.json.return_value = {
            "name": "London", "sys": {"country": "GB"},
            "main": {"temp": 20, "feels_like": 19, "humidity": 55},
            "wind": {"speed": 4}, "weather": [{"description": "clear sky"}]
        }
        self.session.get.return_value = self.response

    def test_success_and_request_parameters(self):
        data = get_weather(" London ", "fake-test-key", self.session)
        self.assertEqual(data["temp_f"], 68)
        self.assertEqual(data["wind_kmh"], 14.4)
        self.assertEqual(data["humidity"], 55)
        kwargs = self.session.get.call_args.kwargs
        self.assertEqual(kwargs["params"]["q"], "London")
        self.assertEqual(kwargs["params"]["units"], "metric")
        self.assertEqual(kwargs["timeout"], 10)

    def test_invalid_city_and_key(self):
        for city, key in [(" ", "x"), ("a" * 101, "x"), ("Paris", " ")]:
            with self.subTest(city=city), self.assertRaises(WeatherError):
                get_weather(city, key, self.session)
        self.session.get.assert_not_called()

    def test_http_errors(self):
        for status in (401, 404, 429, 500):
            self.response.status_code = status
            with self.subTest(status=status), self.assertRaises(WeatherError):
                get_weather("London", "fake-test-key", self.session)

    def test_network_and_bad_data(self):
        self.session.get.side_effect = requests.Timeout("timed out")
        with self.assertRaisesRegex(WeatherError, "timed out"):
            get_weather("London", "fake-test-key", self.session)
        self.session.get.side_effect = None
        self.response.json.return_value = {"weather": []}
        with self.assertRaisesRegex(WeatherError, "malformed"):
            get_weather("London", "fake-test-key", self.session)

    def test_env_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".env"
            with self.assertRaises(WeatherError):
                read_api_key(path)
            path.write_text('# comment\nOPENWEATHER_API_KEY="demo-key"\n', encoding="utf-8")
            self.assertEqual(read_api_key(path), "demo-key")
            path.write_text("OPENWEATHER_API_KEY=your_api_key_here\n", encoding="utf-8")
            with self.assertRaises(WeatherError):
                read_api_key(path)


if __name__ == "__main__":
    unittest.main()
