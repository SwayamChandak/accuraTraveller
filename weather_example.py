"""
Weather Service - Example Usage
Demonstrates how to use the weather_service module
"""

from weather_service import WeatherService
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    """Main function demonstrating weather service usage"""
    
    print("\n" + "="*70)
    print("🌤️  WEATHER SERVICE - EXAMPLE USAGE")
    print("="*70 + "\n")
    
    # Initialize weather service
    try:
        # Get API key from environment variable
        api_key = os.getenv('OPENWEATHER_API_KEY')
        
        if not api_key or api_key == 'your_api_key_here':
            print("❌ API Key not found!")
            print("\nSetup Instructions:")
            print("1. Get free API key: https://openweathermap.org/api")
            print("2. Copy .env.example to .env")
            print("3. Add your API key to .env file")
            print("\nOR set environment variable:")
            print("   Windows PowerShell: $env:OPENWEATHER_API_KEY='your_key'")
            print("   Windows CMD: set OPENWEATHER_API_KEY=your_key")
            print("   Linux/Mac: export OPENWEATHER_API_KEY='your_key'")
            return
        
        weather = WeatherService(api_key=api_key)
        
        # Example 1: Search for multiple locations
        print("📍 Example 1: Find locations named 'London'")
        print("-" * 70)
        locations = weather.get_coordinates("London", limit=3)
        for i, loc in enumerate(locations, 1):
            state_info = f", {loc['state']}" if loc['state'] else ""
            print(f"{i}. {loc['name']}{state_info}, {loc['country']}")
            print(f"   Coordinates: {loc['lat']}, {loc['lon']}")
        print()
        
        # Example 2: Get current weather for a specific city
        print("🌤️  Example 2: Current weather for 'Mumbai, India'")
        print("-" * 70)
        current_weather = weather.get_weather_by_city("Mumbai,IN")
        if current_weather:
            weather.print_current_weather(current_weather)
        
        # Example 3: Get weather using coordinates directly
        print("🌡️  Example 3: Weather by coordinates (Pune)")
        print("-" * 70)
        pune_weather = weather.get_weather(18.5204, 73.8567)  # Pune coordinates
        if pune_weather:
            print(f"Location: {pune_weather['location']}")
            print(f"Temperature: {pune_weather['temperature']['current']}{pune_weather['temperature']['unit']}")
            print(f"Weather: {pune_weather['weather']['description'].title()}")
            print(f"Humidity: {pune_weather['humidity']}%")
            print()
        
        # Example 4: Get weather forecast
        print("📅 Example 4: 3-day weather forecast for 'Goa'")
        print("-" * 70)
        forecast = weather.get_forecast_by_city("Goa,IN", days=3)
        if forecast:
            weather.print_forecast(forecast, days_to_show=3)
        
        # Example 5: Save weather data to JSON
        print("💾 Example 5: Save weather data to file")
        print("-" * 70)
        delhi_weather = weather.get_weather_by_city("Delhi,IN")
        if delhi_weather:
            weather.save_weather_data(delhi_weather, "delhi_weather.json")
            print()
        
        # Example 6: Compare weather in multiple cities
        print("🌍 Example 6: Compare weather in multiple cities")
        print("-" * 70)
        cities = ["Mumbai,IN", "Bangalore,IN", "Pune,IN", "Goa,IN"]
        
        print(f"{'City':<20} {'Temp':<10} {'Weather':<20} {'Humidity':<10}")
        print("-" * 70)
        
        for city in cities:
            city_weather = weather.get_weather_by_city(city)
            if city_weather:
                print(f"{city_weather['location']:<20} "
                      f"{city_weather['temperature']['current']:>5.1f}°C   "
                      f"{city_weather['weather']['description']:<20} "
                      f"{city_weather['humidity']:>5}%")
        print()
        
        print("="*70)
        print("✅ All examples completed successfully!")
        print("="*70 + "\n")
        
    except ValueError as e:
        print(f"❌ Error: {e}\n")
    except Exception as e:
        print(f"❌ Unexpected error: {e}\n")


def travel_weather_check():
    """
    Example: Check weather for travel planning
    This shows how to integrate weather service with travel itinerary
    """
    
    print("\n" + "="*70)
    print("✈️  TRAVEL WEATHER CHECK")
    print("="*70 + "\n")
    
    try:
        api_key = os.getenv('OPENWEATHER_API_KEY')
        weather = WeatherService(api_key=api_key)
        
        # Travel destinations
        destinations = [
            ("Goa", "Beach vacation"),
            ("Manali", "Mountain retreat"),
            ("Jaipur", "Cultural tour")
        ]
        
        print("Planning your trip? Check the weather!\n")
        
        for city, purpose in destinations:
            print(f"📍 {city} - {purpose}")
            print("-" * 70)
            
            current = weather.get_weather_by_city(f"{city},IN")
            if current:
                temp = current['temperature']['current']
                condition = current['weather']['description']
                humidity = current['humidity']
                
                print(f"Current: {temp}°C, {condition.title()}, Humidity: {humidity}%")
                
                # Give recommendations based on weather
                if temp > 30:
                    print("🌞 Hot weather - Pack light clothes, sunscreen, stay hydrated")
                elif temp < 15:
                    print("🧥 Cool weather - Pack warm clothes, jackets")
                else:
                    print("👌 Pleasant weather - Perfect for outdoor activities")
                
                if current['weather']['main'] == 'Rain':
                    print("🌧️  Rainy - Don't forget umbrella and raincoat!")
                elif humidity > 70:
                    print("💧 High humidity - Can feel sticky")
                
                print()
        
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    # Run basic examples
    main()
    
    # Run travel planning example
    travel_weather_check()
