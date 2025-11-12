"""
Weather Service Module
Uses OpenWeatherMap API to get weather data for any city
- Geocoding: Convert city name to lat/lon coordinates
- Weather: Get current weather data using coordinates
"""

import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class WeatherService:
    """
    Weather service to fetch current weather and forecasts using OpenWeatherMap API.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Weather Service.
        
        Args:
            api_key: OpenWeatherMap API key. If not provided, will look for OPENWEATHER_API_KEY env variable
        """
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key is required. Either pass it as parameter or set OPENWEATHER_API_KEY environment variable.\n"
                "Get your free API key from: https://openweathermap.org/api"
            )
        
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        
    def get_coordinates(self, city: str, limit: int = 5) -> List[Dict]:
        """
        Get latitude and longitude coordinates for a city.
        
        Args:
            city: City name (can include state/country, e.g., "London,UK" or "Paris,France")
            limit: Maximum number of results to return (default: 5)
            
        Returns:
            List of dictionaries with location data including lat, lon, name, country
            
        Example:
            >>> weather = WeatherService(api_key="your_key")
            >>> coords = weather.get_coordinates("London")
            >>> print(coords[0])
            {'name': 'London', 'lat': 51.5073219, 'lon': -0.1276474, 'country': 'GB'}
        """
        params = {
            'q': city,
            'limit': limit,
            'appid': self.api_key
        }
        
        try:
            response = requests.get(self.geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                print(f"⚠️  No results found for city: {city}")
                return []
            
            # Format the results
            locations = []
            for location in data:
                locations.append({
                    'name': location.get('name'),
                    'lat': location.get('lat'),
                    'lon': location.get('lon'),
                    'country': location.get('country'),
                    'state': location.get('state', ''),
                })
            
            return locations
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching coordinates: {e}")
            return []
    
    def get_weather(self, lat: float, lon: float, units: str = 'metric') -> Optional[Dict]:
        """
        Get current weather data using latitude and longitude.
        
        Args:
            lat: Latitude
            lon: Longitude
            units: Temperature units ('metric' for Celsius, 'imperial' for Fahrenheit, 'standard' for Kelvin)
            
        Returns:
            Dictionary with weather data or None if error
            
        Example:
            >>> weather = WeatherService(api_key="your_key")
            >>> data = weather.get_weather(51.5074, -0.1278)
            >>> print(f"Temperature: {data['temp']}°C")
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': units
        }
        
        try:
            response = requests.get(self.weather_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract and format relevant weather information
            weather_info = {
                'location': data['name'],
                'country': data['sys']['country'],
                'coordinates': {
                    'lat': data['coord']['lat'],
                    'lon': data['coord']['lon']
                },
                'temperature': {
                    'current': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'min': data['main']['temp_min'],
                    'max': data['main']['temp_max'],
                    'unit': '°C' if units == 'metric' else '°F' if units == 'imperial' else 'K'
                },
                'weather': {
                    'main': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                },
                'wind': {
                    'speed': data['wind']['speed'],
                    'deg': data['wind'].get('deg', 0),
                    'unit': 'm/s' if units == 'metric' else 'mph'
                },
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'clouds': data['clouds']['all'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
                'timestamp': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching weather: {e}")
            return None
    
    def get_weather_by_city(self, city: str, units: str = 'metric') -> Optional[Dict]:
        """
        Get weather data for a city (combines geocoding + weather fetch).
        
        Args:
            city: City name (e.g., "London", "Paris,FR", "New York,US")
            units: Temperature units ('metric', 'imperial', or 'standard')
            
        Returns:
            Dictionary with weather data or None if error
            
        Example:
            >>> weather = WeatherService(api_key="your_key")
            >>> data = weather.get_weather_by_city("London")
            >>> print(f"Weather in {data['location']}: {data['weather']['description']}")
        """
        # Step 1: Get coordinates
        locations = self.get_coordinates(city, limit=1)
        
        if not locations:
            return None
        
        location = locations[0]
        print(f"📍 Found: {location['name']}, {location['country']} (Lat: {location['lat']}, Lon: {location['lon']})")
        
        # Step 2: Get weather using coordinates
        weather_data = self.get_weather(location['lat'], location['lon'], units)
        
        return weather_data
    
    def get_forecast(self, lat: float, lon: float, units: str = 'metric', days: int = 5) -> Optional[Dict]:
        """
        Get weather forecast for the next 5 days (3-hour intervals).
        
        Args:
            lat: Latitude
            lon: Longitude
            units: Temperature units ('metric', 'imperial', or 'standard')
            days: Number of days to forecast (max 5 with free API)
            
        Returns:
            Dictionary with forecast data or None if error
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': units
        }
        
        try:
            response = requests.get(self.forecast_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract forecast data
            forecast_list = []
            for item in data['list'][:days * 8]:  # 8 entries per day (3-hour intervals)
                forecast_list.append({
                    'datetime': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                    'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
                    'time': datetime.fromtimestamp(item['dt']).strftime('%H:%M'),
                    'temp': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'weather': item['weather'][0]['main'],
                    'description': item['weather'][0]['description'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed'],
                    'rain_probability': item.get('pop', 0) * 100  # Probability of precipitation
                })
            
            forecast_info = {
                'location': data['city']['name'],
                'country': data['city']['country'],
                'coordinates': {
                    'lat': data['city']['coord']['lat'],
                    'lon': data['city']['coord']['lon']
                },
                'unit': '°C' if units == 'metric' else '°F' if units == 'imperial' else 'K',
                'forecast': forecast_list
            }
            
            return forecast_info
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching forecast: {e}")
            return None
    
    def get_forecast_by_city(self, city: str, units: str = 'metric', days: int = 5) -> Optional[Dict]:
        """
        Get weather forecast for a city.
        
        Args:
            city: City name
            units: Temperature units
            days: Number of days to forecast
            
        Returns:
            Dictionary with forecast data or None if error
        """
        locations = self.get_coordinates(city, limit=1)
        
        if not locations:
            return None
        
        location = locations[0]
        return self.get_forecast(location['lat'], location['lon'], units, days)
    
    def print_current_weather(self, weather_data: Dict):
        """
        Print formatted current weather information.
        
        Args:
            weather_data: Weather data dictionary from get_weather() or get_weather_by_city()
        """
        if not weather_data:
            print("No weather data to display")
            return
        
        print("\n" + "="*60)
        print(f"🌤️  CURRENT WEATHER: {weather_data['location']}, {weather_data['country']}")
        print("="*60)
        print(f"📅 Time: {weather_data['timestamp']}")
        print(f"📍 Coordinates: {weather_data['coordinates']['lat']}, {weather_data['coordinates']['lon']}")
        print()
        print(f"🌡️  Temperature: {weather_data['temperature']['current']}{weather_data['temperature']['unit']}")
        print(f"   Feels like: {weather_data['temperature']['feels_like']}{weather_data['temperature']['unit']}")
        print(f"   Min: {weather_data['temperature']['min']}{weather_data['temperature']['unit']} | Max: {weather_data['temperature']['max']}{weather_data['temperature']['unit']}")
        print()
        print(f"☁️  Condition: {weather_data['weather']['main']} - {weather_data['weather']['description'].title()}")
        print(f"💧 Humidity: {weather_data['humidity']}%")
        print(f"🌬️  Wind: {weather_data['wind']['speed']} {weather_data['wind']['unit']}")
        print(f"👁️  Visibility: {weather_data['visibility']:.1f} km")
        print(f"☁️  Cloud Cover: {weather_data['clouds']}%")
        print(f"🌅 Sunrise: {weather_data['sunrise']}")
        print(f"🌇 Sunset: {weather_data['sunset']}")
        print("="*60 + "\n")
    
    def print_forecast(self, forecast_data: Dict, days_to_show: int = 3):
        """
        Print formatted weather forecast.
        
        Args:
            forecast_data: Forecast data from get_forecast() or get_forecast_by_city()
            days_to_show: Number of days to display
        """
        if not forecast_data:
            print("No forecast data to display")
            return
        
        print("\n" + "="*60)
        print(f"📅 WEATHER FORECAST: {forecast_data['location']}, {forecast_data['country']}")
        print("="*60)
        
        # Group by date
        daily_forecasts = {}
        for item in forecast_data['forecast']:
            date = item['date']
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(item)
        
        # Display forecast for each day
        for idx, (date, forecasts) in enumerate(list(daily_forecasts.items())[:days_to_show]):
            print(f"\n📆 {date}")
            print("-" * 60)
            
            # Get daily summary
            temps = [f['temp'] for f in forecasts]
            conditions = [f['weather'] for f in forecasts]
            rain_probs = [f['rain_probability'] for f in forecasts]
            
            print(f"🌡️  Temp Range: {min(temps):.1f}{forecast_data['unit']} - {max(temps):.1f}{forecast_data['unit']}")
            print(f"☁️  Conditions: {', '.join(set(conditions))}")
            print(f"🌧️  Rain Probability: {max(rain_probs):.0f}%")
            print()
            
            # Show 3-hour intervals
            for forecast in forecasts[:4]:  # Show first 4 intervals (12 hours)
                print(f"  {forecast['time']}: {forecast['temp']:.1f}{forecast_data['unit']}, {forecast['description']}")
        
        print("="*60 + "\n")
    
    def save_weather_data(self, weather_data: Dict, filename: str = "weather_data.json"):
        """
        Save weather data to JSON file.
        
        Args:
            weather_data: Weather data dictionary
            filename: Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(weather_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Weather data saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving weather data: {e}")


# Example usage and testing
if __name__ == "__main__":
    print("="*60)
    print("OpenWeatherMap API - Weather Service")
    print("="*60)
    print("\n⚠️  SETUP REQUIRED:")
    print("1. Get free API key from: https://openweathermap.org/api")
    print("2. Set environment variable: OPENWEATHER_API_KEY=your_api_key")
    print("   OR pass API key when creating WeatherService(api_key='your_key')")
    print("\n" + "="*60 + "\n")
    
    # Example usage (replace 'your_api_key' with actual key)
    try:
        # Initialize service
        # Option 1: Using environment variable
        # weather_service = WeatherService()
        
        # Option 2: Direct API key
        API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
        weather_service = WeatherService(api_key=API_KEY)
        
        # Example 1: Get coordinates for a city
        print("📍 Example 1: Get coordinates for 'London'")
        locations = weather_service.get_coordinates("London", limit=3)
        for loc in locations:
            print(f"  • {loc['name']}, {loc['country']} - Lat: {loc['lat']}, Lon: {loc['lon']}")
        print()
        
        # Example 2: Get weather by coordinates
        if locations:
            print("🌤️  Example 2: Get weather by coordinates")
            weather = weather_service.get_weather(locations[0]['lat'], locations[0]['lon'])
            if weather:
                weather_service.print_current_weather(weather)
        
        # Example 3: Get weather by city name (easiest method)
        print("🌤️  Example 3: Get weather by city name")
        weather = weather_service.get_weather_by_city("Paris")
        if weather:
            weather_service.print_current_weather(weather)
            weather_service.save_weather_data(weather, "paris_weather.json")
        
        # Example 4: Get weather forecast
        print("📅 Example 4: Get 3-day forecast")
        forecast = weather_service.get_forecast_by_city("Tokyo", days=3)
        if forecast:
            weather_service.print_forecast(forecast, days_to_show=3)
        
    except ValueError as e:
        print(f"\n❌ {e}")
        print("\nTo use this module:")
        print("1. Get API key from: https://openweathermap.org/api")
        print("2. Run: export OPENWEATHER_API_KEY='your_key'  (Linux/Mac)")
        print("   OR:  set OPENWEATHER_API_KEY=your_key      (Windows CMD)")
        print("   OR:  $env:OPENWEATHER_API_KEY='your_key'   (Windows PowerShell)")
