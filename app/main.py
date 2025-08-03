
import json
import requests
import streamlit as st

# Welcome message when lunching the Weather Checker app
print("Hello from Weather Checker!")

# Reading API key from the external config file (config.json)
api_key = st.secrets["api_key"]


while True:
    user_city = input("Please enter your city name:\n")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={user_city.lower()}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        break
    else:
        print("City not found! Please try again\n", user_city)

data = response.json()
city = data ["name"]
country = data["sys"]["country"]
description = data["weather"][0]["description"]
temp = data["main"]["temp"]
temp_celsius = round(temp - 273.15, 1)
humidity = data["main"]["humidity"]
print(f"Weather in {city}, {country}:\n{description}\nTemperature:{temp_celsius}\u00B0C\nHumidity:{humidity}%")


