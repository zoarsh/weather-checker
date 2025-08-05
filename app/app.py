import streamlit as st

# Step 1: Language selection
language = st.selectbox("Select language / בחר שפה", ["English", "עברית"])

# Step 2: Define multilingual text dictionary
texts = {
    "English": {
        "title": "Weather App",
        "enter_name": "Enter your name",
        "welcome": "Hello {name}, welcome to Zohar`s Weather Checker!!",
        "description": "This is your one-stop app for real-time weather updates around the globe.<br>Just type in the name of any city, hit the button, and instantly get the current temperature, weather description, and local time.<br>All in one place!!<br>Fast, simple, and always up to date!"
        "ask_city": "Which city would you like to check?",
        "button": "Check Weather",
        "not_found": "City not found! Please try again.",
        "weather": "Weather in {city}, {country}:",
        "temperature": "Temperature",
        "humidity": "Humidity",
    },
    "עברית": {
        "title": "אפליקציית מזג אוויר",
        "enter_name": "הכנס את שמך",
        "welcome": "שלום {name},ברוך הבא לבדיקת מזג האוויר של זהר!",
        "description": "כאן תוכל לקבל מידע עדכני בזמן אמת על מזג האוויר בעולם.\nפשוט הקלד שם של עיר, לחץ על הכפתור ותקבל את הטמפרטורה הנוכחית, תיאור מזג האוויר והשעה המקומית.\nמהיר, פשוט ותמיד עדכני!",
        "ask_city": "איזו עיר תרצה לבדוק?",
        "button": "בדוק מזג אוויר",
        "not_found": "העיר לא נמצאה! נסה שוב.",
        "weather": " מזג האוויר ב {city}, {country}:",
        "temperature": "טמפרטורה",
        "humidity": "לחות",
    }
}
description_translations = {
    "clear sky": "שמיים בהירים",
    "few clouds": "מעט עננים",
    "scattered clouds": "עננים מפוזרים",
    "broken clouds": "עננות שבורה",
    "shower rain": "גשם מקומי",
    "rain": "גשם",
    "thunderstorm": "סופת רעמים",
    "snow": "שלג",
    "mist": "ערפל",
}

st.title(texts[language]["title"])
name = st.text_input(texts[language]["enter_name"], "")

if name:
    st.subheader(texts[language]["welcome"].format(name=name))

#opening title
st.markdown(texts[language]["description"])
st.divider()
user_city= st.text_input(texts[language]["ask_city"])

from main import load_api_key, fetch_weather, extract_weather_info

api_key = load_api_key()

if st.button(texts[language]["button"]):
    data = fetch_weather(user_city, api_key)
    if data:
        weather_info = extract_weather_info(data)
        st.markdown(f"\n{texts[language]['weather'].format(city=weather_info['city'], country=weather_info['country'])}")
        description = weather_info['description']
        if language == "עברית":
            description = description_translations.get(description, description)

        st.markdown(description)
        st.success(f"{texts[language]['temperature']}: {weather_info['temperature']}°C")
        st.write(f"{texts[language]['humidity']}: {weather_info['humidity']}%")
    else:
        st.warning(texts[language]["not_found"])