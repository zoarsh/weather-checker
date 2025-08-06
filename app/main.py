import json
import requests
import streamlit as st
from datetime import datetime

# =============================
# CONFIGURATION: Load API Key
# =============================
def load_api_key():
    """
    Load the OpenWeatherMap API key from Streamlit secrets.

    Returns:
        str: The API key used for authenticating API requests.
    """

    return st.secrets["api_key"]

# ====================
#  Fetch Weather Data
# ====================
def fetch_weather(city: str, api_key: str) -> dict | None:
    """
    Fetch current weather and 5-day forecast (3-hour intervals) for a specific city.
    """
    # Current weather
    current_url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&units=metric"
        f"&appid={api_key}"
    )

    # Request Validation
    try:
        current_resp = requests.get(current_url)
        current_resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Failed to fetch current weather:", e)
        return None

    current_data = current_resp.json()

    # 5-day forecast
    forecast_url = (
        f"http://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}"
        f"&units=metric"
        f"&appid={api_key}"
    )

    # Request Validation
    try:
        forecast_resp = requests.get(forecast_url)
        forecast_resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Failed to fetch forecast:", e)
        return None

    forecast_data = forecast_resp.json()

    return {
        "city":        current_data["name"],
        "country":     current_data["sys"]["country"],
        "temperature": current_data["main"]["temp"],
        "description": current_data["weather"][0]["description"],
        "humidity":    current_data["main"]["humidity"],
        "wind_speed":  current_data["wind"]["speed"],
        "wind_deg":    current_data["wind"]["deg"],
        "forecast":    forecast_data["list"],  # 3-hour segments
    }



# =============================
# Extract & Format Weather Data
# =============================
def extract_weather_info(data):
    """
    Prepare weather information for display based on current + forecast data.
    """
    return {
        "city":        data.get("city", ""),
        "country":     data.get("country", ""),
        "temperature": data["temperature"],
        "description": data["description"],
        "humidity":    data["humidity"],
        "wind_speed":  data["wind_speed"],
        "wind_deg":    data["wind_deg"],
        "forecast":    data.get("forecast", []),
    }


# =============================
# DISPLAY: Print Results
# =============================
def display_weather(info):
    """
    Display current and 5-day forecast (every 3 hours).
    """
    print(f"\nWeather in {info['city']}, {info['country']}")
    print(f"Now: {info['description']}, {info['temperature']}°C")
    print(f"Humidity: {info['humidity']}% | Wind: {info['wind_speed']} km/h")

    print("\n5-Day Forecast (3-hour intervals):")
    for entry in info["forecast"][:10]:
        dt = datetime.fromtimestamp(entry["dt"]).strftime("%a %H:%M")
        temp = entry["main"]["temp"]
        desc = entry["weather"][0]["description"]
        print(f"{dt} | {desc} | {temp}°C")

# =================
# MAIN FUNCTION
# =================
def main():
    """
      Main function to run the weather checker in console mode.

      - Prompts the user to enter a city name.
      - Loads the API key
      - Fetches weather data for the specified city.
      - If data is found, extracts relevant weather info and displays it.
      - Otherwise, informs the user the city was not found.
      """
    print("Hello from Weather Checker!")
    api_key = load_api_key()

    while True:
        user_city = input("\nPlease enter your city name:\n")
        data = fetch_weather(user_city, api_key)
        print(data)

        if data:
            weather_info = extract_weather_info(data)
            display_weather(weather_info)
            break
        else:
            print("City not found! Please try again.")


# =============
# RUN
# =============
if __name__ == "__main__":
    main()
