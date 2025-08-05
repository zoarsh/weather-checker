import json
import requests


# =============================
# CONFIGURATION: Load API Key
# =============================
def load_api_key(path="app/config.json"):
    """
    Load the OpenWeatherMap API key from a JSON configuration file.

    Parameters:
        path (str): Path to the configuration file (default is 'app/config.json').

    Returns:
        str: The API key used for authenticating API requests.
    """
    with open(path) as f:
        config = json.load(f)
    return config["api_key"]


# =============================
# API REQUEST: Fetch Weather Data
# =============================
def fetch_weather(city, api_key):
    """
       Fetch weather data from the OpenWeatherMap API for a specific city.

       Parameters:
           city (str): The name of the city to retrieve weather data for.
           api_key (str): The API key used for authentication.

       Returns:
           dict or None: The API response as a dictionary if successful, or None if the request fails.
       """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city.lower()}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# =============================
# PROCESSING: Extract & Format Weather Data
# =============================
def extract_weather_info(data):
    """
        Extract relevant weather information from the raw API response.

        Parameters:
            data (dict): Raw data returned from the weather API.

        Returns:
            dict: A dictionary containing extracted weather details (e.g., temperature, humidity, description, location).
        """
    city = data["name"]
    country = data["sys"]["country"]
    description = data["weather"][0]["description"]
    temp_k = data["main"]["temp"]
    temp_celsius = round(temp_k - 273.15, 1)
    humidity = data["main"]["humidity"]

    return {
        "city": city,
        "country": country,
        "description": description,
        "temperature": temp_celsius,
        "humidity": humidity
    }


# =============================
# DISPLAY: Print Results
# =============================
def display_weather(info):
    """
        Display the weather information in a user-friendly format.

        Parameters:
            info (dict): A dictionary containing formatted weather information.

        Returns:
            None
        """
    print(f"\nWeather in {info['city']}, {info['country']}:")
    print(info['description'])
    print(f"Temperature: {info['temperature']}°C")
    print(f"Humidity: {info['humidity']}%")


# =============================
# MAIN FUNCTION
# =============================
def main():
    """
      Main function to run the weather checker in console mode.

      - Prompts the user to enter a city name.
      - Loads the API key from the config file.
      - Fetches weather data for the specified city.
      - If data is found, extracts relevant weather info and displays it.
      - Otherwise, informs the user the city was not found.
      """
    print("Hello from Weather Checker!")
    api_key = load_api_key()

    while True:
        user_city = input("\nPlease enter your city name:\n")
        data = fetch_weather(user_city, api_key)

        if data:
            weather_info = extract_weather_info(data)
            display_weather(weather_info)
            break
        else:
            print("City not found! Please try again.")


# =============================
# RUN
# =============================
if __name__ == "__main__":
    main()
