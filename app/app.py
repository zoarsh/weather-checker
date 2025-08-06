# ==========================================
# STREAMLIT APP: Weather Checker UI (app.py)
# ==========================================

import streamlit as st
from datetime import datetime
from main import load_api_key, fetch_weather, extract_weather_info

# ================================
# Custom Page Width – Full Width
# ================================
st.markdown("""
    <style>
        .block-container {
            max-width: 100% !important;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)


# ================================
# Custom Styling for Input Section
# =================================
st.markdown("""
    <style>
        .input-box-container {
            background-color: #f3e5f5;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        .input-row {
            display: flex;
            justify-content: center;
            gap: 40px;
        }
        .input-col {
            flex: 1;
            max-width: 300px;
        }
        .input-col label {
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# =============================
# Language and City Selection
# =============================

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("**Select Language / שפה**")
    language = st.selectbox("", ["English", "עברית"], key="lang_select")

with col2:
    st.markdown("**City / עיר**")
    city = st.text_input("", key="city_input")


# Weather Check Button
st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
clicked = st.button("Check Weather")
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ===================================
# Define multilingual Text Dictionary
# ===================================

texts = {
    "English": {
        "button": "Check Weather",
        "not_found": "City not found! Please try again.",
        "weather": "Weather in {city}, {country}:",
        "temperature": "Temperature",
        "humidity": "Humidity",
    },
    "עברית": {
        "button": "בדיקת התחזית היומית",
        "not_found": "העיר לא נמצאה! נא לנסות שוב.",
        "weather": " התחזית היומית בעיר {city}, {country}:",
        "temperature": "הטמפרטורה בשעות הקרובות",
        "humidity": "הלחות בשעות הקרובות",
    }
}

# ===========================
# Direction and Text Alignment
# ===========================

if language == "עברית":
    direction = "rtl"
    align = "right"
else:
    direction = "ltr"
    align = "left"

# ================================
# Weather Description Translations
# ================================

description_translations = {
    "clear sky": "שמיים בהירים",
    "few clouds": "מעונן קלות",
    "scattered clouds": "מעונן חלקית",
    "broken clouds": "מעונן",
    "shower rain": "גשם מקומי",
    "rain": "גשם",
    "thunderstorm": "סופת רעמים",
    "snow": "שלג",
    "mist": "ערפל",
}
# Weather Emojis by Description
weather_emojis = {
    "clear sky": "☀️",
    "few clouds": "🌤️",
    "scattered clouds": "⛅",
    "broken clouds": "☁️",
    "shower rain": "🌦️",
    "rain": "🌧️",
    "thunderstorm": "🌩️",
    "snow": "❄️",
    "mist": "🌫️",
}

# =========================================
# Display main title with emoji and Info Box
# =========================================

# Add date in desired format
today_short = datetime.now().strftime("%d.%m.%y")

static_emoji = "🌤️"
main_titles = {
    "English": f" Your Daily Weather Check - {today_short}",
    "עברית": f"{today_short} - התחזית היומית שלך"
}

# Format title with emoji
full_title = (
    f"{main_titles[language]} {static_emoji}" if language == "עברית"
    else f"{static_emoji} {main_titles[language]}"
)

# Display the title with correct alignment
st.markdown(
    f"<h1 style='text-align:{align}; color:#6A0DAD;'>{full_title}</h1>",
    unsafe_allow_html=True
)

# description box – HTML per language
app_html = {
    "English": f"""
        <div style='background-color:#f3e5f5; padding:15px; border-radius:10px; direction:ltr; text-align:left; width:100%;'>
            <h4 style='color:#4a148c; text-align:left;'>About this app</h4>
            <p style='text-align:left;'>
            This is your one-stop app for real-time weather updates around the globe. Just type in the name of any city, hit the button, and instantly get:<br>
            – Current temperature 🌡️<br>
            – Weather description 🌤️<br>
            – Local time 🕒<br>
            All in one place – fast, simple, and always up to date!
            </p>
        </div>
    """,
    "עברית": f"""
        <div style='background-color:#f3e5f5; padding:15px; border-radius:10px; direction:rtl; text-align:right; width:100%;'>
            <h4 style='color:#4a148c; text-align:right;'>על האפליקציה</h4>
            <p style='text-align:right;'>
            זוהי אפליקציה פשוטה ומעודכנת לבדיקת תחזית מזג האוויר בכל עיר בעולם בזמן אמת. כל מה שצריך הוא להקליד שם של עיר, ללחוץ על הכפתור ולקבל מיד:<br>
            – טמפרטורה נוכחית 🌡️<br>
            – תיאור מזג האוויר 🌤️<br>
            – שעה מקומית 🕒<br>
            הכל במקום אחד – מהיר, פשוט ותמיד עדכני!
            </p>
        </div>
    """
}


# Display the info box
st.markdown(app_html[language], unsafe_allow_html=True)


# =============================
# City Name for Weather Lookup
# =============================

user_city = city

# ======================================
# Fetch and Display Weather Information
# ======================================

api_key = load_api_key()

if clicked:
    # API Response and data extraction
    data = fetch_weather(user_city, api_key)
    #st.write("API response:", data)
    if data:
        weather_info = extract_weather_info(data)

        # Display dynamic second title with weather emoji and city/country
        emoji = weather_emojis.get(weather_info['description'], "🌤️")

        if language == "עברית":
            city_country = f"<span dir='ltr'>{weather_info['city']}, {weather_info['country']}</span>"
            dynamic_title = f"  {emoji} {city_country} התחזית להיום ב"
        else:
            dynamic_title = f"The forecast today in {weather_info['city']}, {weather_info['country']} is: {emoji}"

        st.markdown(
            f"<h2 style='text-align:center; color:#6A0DAD; font-size:36px;'>{dynamic_title}</h2>",
            unsafe_allow_html=True
        )

        # ========================================
        # Display Time, Temperature & Description
        # =========================================

        now = datetime.now().strftime("%H:%M")
        today_str = datetime.now().strftime("%A, %d %B %Y")

        st.divider()

        # Display date and time – aligned
        if language == "עברית":
            st.markdown(f"""
                <p style='font-size: 24px; font-weight: bold; margin: 0; direction: rtl; text-align: right;'>
                    התאריך היום: {today_str}
                </p>
                <p style='font-size: 28px; font-weight: bold; margin: 0; direction: rtl; text-align: right;'>
                    השעה עכשיו היא: {now} 🕒
                </p>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <p style='font-size: 22px; font-weight: bold; margin: 0; text-align: left;'>
                    Today is {today_str}
                </p>
                <p style='font-size: 22px; font-weight: bold; margin: 0; text-align: left;'>
                    Current time: {now} 🕒
                </p>
            """, unsafe_allow_html=True)

        #======================================================
        # Weather Info Bar – Horizontal display of key metrics
        #======================================================

        # Translate description if needed
        description = weather_info['description']
        if language == "עברית":
            description = description_translations.get(description, description)
            wind_label = "כיוון הרוח"
            temp_label = "הטמפרטורה בשעות הקרובות"
            humidity_label = "הלחות בשעות הקרובות"
        else:
            wind_label = "Wind Direction"
            temp_label = "Temperature in upcoming hours"
            humidity_label = "Humidity in upcoming hours"

        # Get emoji
        emoji = weather_emojis.get(weather_info['description'], "🌤️")

        # Build info bar with styled layout
        col1, col2, col3, col4 = st.columns(4)

        # Weather description
        with col1:
            description = weather_info['description']
            if language == "עברית":
                description = description_translations.get(description, description)
            emoji = weather_emojis.get(weather_info['description'], "🌤️")
            st.markdown(f"""
                            <div style='display: flex; flex-direction: column; align-items: center;'>
                                <div style='font-size: 52px;'>{emoji}</div>
                                <div style='font-size: 24px; font-weight: bold;'>{description}</div>
                            </div>
                        """, unsafe_allow_html=True)

        # Temperature
        with col2:
            st.markdown("""
                            <div style='display: flex; flex-direction: column; align-items: center;'>
                                <div style='font-size: 52px;'>🌡️</div>
                                <div style='font-size: 32px; font-weight: bold;'>""" + f"{weather_info['temperature']}°C" + """</div>
                                <div style='font-size: 20px; font-weight: 600;'>""" + texts[language]["temperature"] + """</div>
                            </div>
                        """, unsafe_allow_html=True)

        # Humidity
        with col3:
            st.markdown("""
                <div style='display: flex; flex-direction: column; align-items: center;'>
                    <div style='font-size: 52px;'>💧</div>
                    <div style='font-size: 32px; font-weight: bold;'>""" + f"{weather_info['humidity']}%" + """</div>
                    <div style='font-size: 20px; font-weight: 600;'>""" + texts[language]["humidity"] + """</div>
                </div>
            """, unsafe_allow_html=True)
        # Wind Direction
        with col4:
            wind_label = "כיוון הרוח" if language == "עברית" else "Wind Direction"
            st.markdown("""
                <div style='display: flex; flex-direction: column; align-items: center;'>
                    <div style='font-size: 52px;'>🌬️</div>
                    <div style='font-size: 32px; font-weight: bold;'>""" + f"{weather_info['wind_deg']}°" + """</div>
                    <div style='font-size: 20px; font-weight: 600;'>""" + wind_label + """</div>
                </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ================================
        # Forecast Display – 5 Days Ahead
        # ================================

        forecast_title = (
            "📅 5-Day Forecast (3-hour intervals)"
            if language == "English"
            else "📅 תחזית ל־5 ימים (במקטעים של 3 שעות)"
        )

        st.markdown(
            f"<h3 style='text-align:{align}; direction:{direction}; color:#4a148c; font-size:28px;'>{forecast_title}</h3>",
            unsafe_allow_html=True
        )

        st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

        # Render forecast entries – (next 5 days)
        last_date = None  # Track last date to group by day

        for idx, entry in enumerate(weather_info["forecast"][:40]):
            forecast_time = entry["dt_txt"]
            dt = datetime.strptime(forecast_time, "%Y-%m-%d %H:%M:%S")
            date_only = dt.date()
            hour_only = dt.strftime("%H:%M")
            temp = entry["main"]["temp"]
            description = entry["weather"][0]["description"]
            icon_code = entry["weather"][0]["icon"]
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

            # Translate description if needed
            if language == "עברית":
                description = description_translations.get(description, description)

            # Add new date heading if it's a new date

            # Hebrew date format, compatible with Windows
            weekday_names = {
                "Sunday": "יום ראשון",
                "Monday": "יום שני",
                "Tuesday": "יום שלישי",
                "Wednesday": "יום רביעי",
                "Thursday": "יום חמישי",
                "Friday": "יום שישי",
                "Saturday": "יום שבת"
            }

            month_names = {
                "January": "ינואר",
                "February": "פברואר",
                "March": "מרץ",
                "April": "אפריל",
                "May": "מאי",
                "June": "יוני",
                "July": "יולי",
                "August": "אוגוסט",
                "September": "ספטמבר",
                "October": "אוקטובר",
                "November": "נובמבר",
                "December": "דצמבר"
            }

            dt = datetime.strptime(forecast_time, "%Y-%m-%d %H:%M:%S")
            if date_only != last_date:
                last_date = date_only
                if language == "עברית":
                    hebrew_date = f"{weekday_names[dt.strftime('%A')]}, {dt.day} ב{month_names[dt.strftime('%B')]}"
                    date_heading = f"📆 {hebrew_date}"
                else:
                    date_heading = f"📆 {dt.strftime('%A')}, {dt.strftime('%B')} {dt.day}"


                st.markdown(
                    f"<h4 style='margin-top:24px; margin-bottom:6px; color:#6A0DAD; direction:{direction}; text-align:{align};'>{date_heading}</h4>",
                    unsafe_allow_html=True
                )

            # Alternate row background color
            bg_color = "#f9f9f9" if idx % 2 == 0 else "#eeeeee"

            with st.container():
                st.markdown(
                    f"<div style='background-color:{bg_color}; padding:10px; border-radius:10px;'>",
                    unsafe_allow_html=True
                )

                col1, col2, col3 = st.columns([1, 2, 5])

                with col1:
                    # Get matching emoji for description
                    emoji = weather_emojis.get(description, "🌤️")

                    # Display emoji as icon
                    st.markdown(
                        f"<div style='font-size: 36px; text-align: center;'>{emoji}</div>",
                        unsafe_allow_html=True
                    )

                with col2:
                    # Forecast time
                    with col2:

                        # Convert full timestamp to hour only
                        hour_only = datetime.strptime(forecast_time, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")

                        # Display centered large hour
                        st.markdown(
                            f"<div style='font-size: 28px; font-weight: bold; text-align: center;'>{hour_only}</div>",
                            unsafe_allow_html=True
                        )

                with col3:
                    # Description and temperature
                    st.markdown(
                        f"<div style='font-size: 18px; direction:{direction}; text-align:{align};'>"
                        f"{description}, <strong>{temp:.1f}°C</strong>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

            st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

        st.divider()





