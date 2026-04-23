import requests
from datetime import datetime, timedelta

class WeatherService:

    def get_coordinates(self, plz: str) -> dict:
        url = f"https://api.zippopotam.us/de/{plz}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise ValueError(f"PLZ '{plz}' nicht gefunden.")

        data = response.json()
        place = data["places"][0]

        return {
            "lat": float(place["latitude"]),
            "lon": float(place["longitude"]),
            "city": place["place name"]
        }

    def get_weather(self, lat: float, lon: float, date: str) -> dict:
        start_date = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=6)
        start_date = start_date.strftime("%Y-%m-%d")

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&daily=precipitation_sum,temperature_2m_max,sunshine_duration"
            f"&start_date={start_date}&end_date={date}"
            f"&timezone=Europe/Berlin"
        )
        response = requests.get(url, timeout=10)
        data = response.json()

        return {
            "precipitation_total": sum(data["daily"]["precipitation_sum"]),
            "precipitation_daily": data["daily"]["precipitation_sum"],
            "temperature_avg": round(sum(data["daily"]["temperature_2m_max"]) / 7, 1),
            "temperature_daily": data["daily"]["temperature_2m_max"],
            "sunshine_daily": data["daily"]["sunshine_duration"]
        }

    def get_weather_for_city(self, city: str, date: str) -> dict:
        coords = self.get_coordinates(city)
        weather = self.get_weather(coords["lat"], coords["lon"], date)

        return {
            "city": coords["city"],
            "date": date,
            "precipitation_total": weather["precipitation_total"],
            "precipitation_daily": weather["precipitation_daily"],
            "temperature_avg": weather["temperature_avg"],
            "temperature_daily": weather["temperature_daily"],
            "season": self._get_season(date),
            "sunshine_daily": weather["sunshine_daily"]
        }

    def _get_season(self, date: str) -> str:
        month = datetime.strptime(date, "%Y-%m-%d").month

        if month in [3, 4, 5]:
            return "Frühling"
        elif month in [6, 7, 8]:
            return "Sommer"
        elif month in [9, 10, 11]:
            return "Herbst"
        else:
            return "Winter"