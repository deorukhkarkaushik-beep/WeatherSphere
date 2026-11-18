
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from textwrap import dedent
from datetime import date

# =====================================================
# WEATHER VISION AI - VERSION 3.0
# =====================================================

st.set_page_config(
    page_title="WeatherVision AI",
    page_icon="🌦️",
    layout="wide"
)

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: Inter, sans-serif;
}

.stApp {
    background: linear-gradient(135deg,#e3f3ff,#f4faff,#d9ecff);
    color: #153c64;
}

.block-container {
    max-width: 1500px;
    padding: 1.5rem 2rem;
}

.brand {
    font-size: 27px;
    font-weight: 800;
    color: #153c64;
}

.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #173e65;
    margin: 20px 0 12px;
}

.forecast-card {
    background: linear-gradient(150deg,#ffffff,#e8f5ff);
    border: 1px solid #c8e2f5;
    border-radius: 18px;
    padding: 13px 5px;
    text-align: center;
    min-height: 150px;
    transition: .3s;
    animation: appear .7s ease;
}

.forecast-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 25px #8dbbd744;
}

.weather-icon {
    font-size: 34px;
    margin: 12px 0;
    animation: float 3s infinite ease-in-out;
}

.forecast-temp {
    color: #153c64;
    font-size: 23px;
    font-weight: 800;
}

.city-card {
    background: #ffffff;
    border: 1px solid #d4e7f6;
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 10px;
}

.hero {
    background: linear-gradient(120deg,#d6efff,#a9d9f5);
    border: 1px solid #b8ddf5;
    border-radius: 20px;
    padding: 22px;
    color: #153c64;
    margin: 15px 0;
}

.hero-temp {
    font-size: 54px;
    font-weight: 800;
}

.stButton button {
    background: linear-gradient(90deg,#2563eb,#38bdf8);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
}

.stButton button:hover {
    color: white;
    background: #1d4ed8;
}

.stTextInput input {
    background: white !important;
    color: #153c64 !important;
    border-radius: 12px !important;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #d4e7f6;
    border-radius: 14px;
    padding: 12px;
}

div[data-testid="stMetricValue"] {
    color: #153c64 !important;
}

@keyframes float {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

@keyframes appear {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

footer {visibility:hidden;}
#MainMenu {visibility:hidden;}
</style>
""", unsafe_allow_html=True)


# =====================================================
# WEATHER CONDITIONS
# =====================================================

def weather_info(code):

    mapping = {
        0: ("☀️", "Clear Sky"),
        1: ("🌤️", "Mainly Clear"),
        2: ("⛅", "Partly Cloudy"),
        3: ("☁️", "Cloudy"),
        45: ("🌫️", "Foggy"),
        48: ("🌫️", "Foggy"),
        51: ("🌦️", "Light Drizzle"),
        53: ("🌦️", "Drizzle"),
        55: ("🌧️", "Heavy Drizzle"),
        61: ("🌧️", "Light Rain"),
        63: ("🌧️", "Rainy"),
        65: ("🌧️", "Heavy Rain"),
        71: ("🌨️", "Snow"),
        73: ("❄️", "Snowy"),
        75: ("❄️", "Heavy Snow"),
        80: ("🌦️", "Rain Showers"),
        81: ("🌧️", "Heavy Showers"),
        82: ("⛈️", "Storm"),
        95: ("⛈️", "Thunderstorm"),
        96: ("⛈️", "Thunderstorm"),
        99: ("⛈️", "Severe Storm")
    }

    return mapping.get(int(code), ("🌤️", "Unknown"))


# =====================================================
# DYNAMIC WEATHER PHOTOGRAPHS
# =====================================================

def weather_photo(code, temperature):

    code = int(code)
    temperature = float(temperature)

    # Rain and monsoon
    if code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]:
        return (
            "https://images.unsplash.com/"
            "photo-1519692933481-e162a57d6721"
            "?auto=format&fit=crop&w=1400&q=85"
        ), "🌧️ Rainy Weather"

    # Snow and winter
    if code in [71, 73, 75]:
        return (
            "https://images.unsplash.com/"
            "photo-1478265409131-1f65c88f965c"
            "?auto=format&fit=crop&w=1400&q=85"
        ), "❄️ Winter Weather"

    if temperature <= 12:
        return (
            "https://images.unsplash.com/"
            "photo-1418985991508-e47386d96a71"
            "?auto=format&fit=crop&w=1400&q=85"
        ), "❄️ Cold Weather"

    # Clouds
    if code in [2, 3, 45, 48]:
        return (
            "https://images.unsplash.com/"
            "photo-1534088568595-a066f410bcda"
            "?auto=format&fit=crop&w=1400&q=85"
        ), "☁️ Cloudy Weather"

    # Summer and hot weather
    if temperature >= 30:
        return (
            "https://images.unsplash.com/"
            "photo-1500530855697-b586d89ba3ee"
            "?auto=format&fit=crop&w=1400&q=85"
        ), "☀️ Summer Weather"

    # Sunny weather
    return (
        "https://images.unsplash.com/"
        "photo-1500530855697-b586d89ba3ee"
        "?auto=format&fit=crop&w=1400&q=85"
    ), "🌤️ Pleasant Weather"


# =====================================================
# API FUNCTIONS
# =====================================================

@st.cache_data(ttl=3600)
def search_city(city):

    response = requests.get(
        GEO_URL,
        params={
            "name": city,
            "count": 10,
            "language": "en",
            "format": "json"
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json().get("results", [])


@st.cache_data(ttl=600)
def get_weather(lat, lon):

    response = requests.get(
        WEATHER_URL,
        params={
            "latitude": lat,
            "longitude": lon,

            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,is_day,precipitation,"
                "rain,weather_code,cloud_cover,"
                "pressure_msl,wind_speed_10m,"
                "wind_direction_10m,wind_gusts_10m"
            ),

            "hourly": (
                "temperature_2m,precipitation_probability,"
                "relative_humidity_2m,wind_speed_10m"
            ),

            "daily": (
                "weather_code,temperature_2m_max,"
                "temperature_2m_min,sunrise,sunset,"
                "uv_index_max,precipitation_probability_max"
            ),

            "forecast_days": 16,
            "timezone": "auto"
        },
        timeout=25
    )

    response.raise_for_status()

    return response.json()


@st.cache_data(ttl=1800)
def get_air(lat, lon):

    response = requests.get(
        AIR_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "us_aqi,pm2_5,pm10",
            "timezone": "auto"
        },
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# =====================================================
# DEFAULT LOCATION
# =====================================================

if "place" not in st.session_state:

    st.session_state.place = {
        "name": "Pune",
        "country": "India",
        "latitude": 18.5204,
        "longitude": 73.8567
    }


# =====================================================
# HEADER
# =====================================================

head1, head2, head3 = st.columns([2, 5, 1])

with head1:
    st.markdown(
        '<div class="brand">🌦️ WeatherVision AI</div>'
        '<div style="color:#66809a;font-size:12px;">'
        'GLOBAL WEATHER INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

with head2:
    st.write("")

with head3:
    if st.button("🔄 Refresh"):
        get_weather.clear()
        get_air.clear()
        st.rerun()


# =====================================================
# CITY SEARCH - IMPROVED
# =====================================================

st.markdown("### 🔍 Search Any City")

with st.form("city_search_form"):

    search_input = st.text_input(
        "Enter city name",
        placeholder="Example: Pune, Mumbai, Delhi, London, Tokyo..."
    )

    search_button = st.form_submit_button(
        "Search City 🔎",
        use_container_width=True
    )

if search_button:

    if not search_input.strip():
        st.warning("Please enter a city name.")

    else:

        try:
            with st.spinner("Searching worldwide locations..."):

                results = search_city(search_input.strip())

            if not results:
                st.error(
                    "City not found. Check the spelling and try again."
                )

                st.session_state.pop("search_results", None)

            else:

                # Automatically choose an exact city-name match
                exact = [
                    r for r in results
                    if r["name"].casefold() == search_input.strip().casefold()
                ]

                if len(exact) == 1:

                    st.session_state.place = exact[0]
                    st.session_state.pop("weather_data", None)
                    st.session_state.pop("air_data", None)
                    st.session_state.pop("search_results", None)

                    st.rerun()

                else:
                    st.session_state.search_results = results

        except requests.RequestException as error:
            st.error(f"City search failed: {error}")


# Select the correct location when names are similar

if st.session_state.get("search_results"):

    results = st.session_state.search_results

    labels = [
        f"{r['name']}, {r.get('admin1', '')}, {r['country']}"
        for r in results
    ]

    selected = st.selectbox(
        "Choose the correct city",
        range(len(results)),
        format_func=lambda i: labels[i]
    )

    if st.button("Show Weather for Selected City"):

        st.session_state.place = results[selected]

        st.session_state.pop("weather_data", None)
        st.session_state.pop("air_data", None)
        st.session_state.pop("search_results", None)

        st.rerun()


# =====================================================
# LOAD WEATHER
# =====================================================

place = st.session_state.place

city = place["name"]
country = place.get("country", "")
lat = place["latitude"]
lon = place["longitude"]

try:

    if "weather_data" not in st.session_state:

        with st.spinner(f"Loading weather for {city}..."):

            st.session_state.weather_data = get_weather(lat, lon)

    data = st.session_state.weather_data

except requests.RequestException as error:

    st.error(f"Weather service error: {error}")
    st.stop()

current = data["current"]
daily = data["daily"]
hourly = data["hourly"]


# =====================================================
# DATE SELECTOR
# =====================================================

st.markdown("---")
st.markdown("## 📅 Select Forecast Date")

first_date = date.fromisoformat(daily["time"][0])
last_date = date.fromisoformat(daily["time"][-1])

selected_date = st.date_input(
    "Choose the date for weather prediction",
    value=first_date,
    min_value=first_date,
    max_value=last_date,
    format="DD/MM/YYYY"
)

selected_string = selected_date.isoformat()

date_index = daily["time"].index(selected_string)

selected_code = daily["weather_code"][date_index]
selected_max = daily["temperature_2m_max"][date_index]
selected_min = daily["temperature_2m_min"][date_index]
selected_rain = daily["precipitation_probability_max"][date_index]
selected_uv = daily["uv_index_max"][date_index]

icon, description = weather_info(selected_code)

photo_url, photo_caption = weather_photo(
    selected_code,
    selected_max
)


# =====================================================
# DASHBOARD TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "🌤️ Weather Dashboard",
    "📊 Weather Analytics",
    "🌫️ Air Quality"
])


# =====================================================
# WEATHER DASHBOARD
# =====================================================

with tab1:

    st.markdown(
        f"### 📍 {city}, {country}"
    )

    st.caption(
        f"Forecast date: {selected_date.strftime('%A, %d %B %Y')}"
    )

    # Selected day information

    st.markdown(f"""
    <div class="hero">
        <div style="font-size:15px;font-weight:600;">
            {city} Weather Forecast
        </div>
        <div style="font-size:43px;">{icon}</div>
        <div class="hero-temp">{selected_max:.1f}°C</div>
        <div style="font-size:19px;font-weight:700;">
            {description}
        </div>
        <div style="margin-top:10px;">
            Minimum Temperature: {selected_min:.1f}°C
            <br>
            Rain Probability: {selected_rain}%
            <br>
            UV Index: {selected_uv}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Selected-date weather photograph

    st.image(
        photo_url,
        caption=photo_caption,
        use_container_width=True
    )

    # 16-day forecast displayed in two rows of eight cards

    st.markdown("### 📅 16-Day Weather Forecast")

    for start in range(0, 16, 8):

        forecast_cols = st.columns(8)

        for j, col in enumerate(forecast_cols):

            i = start + j

            if i >= len(daily["time"]):
                break

            day_icon, day_desc = weather_info(
                daily["weather_code"][i]
            )

            forecast_date = pd.to_datetime(
                daily["time"][i]
            )

            day_name = (
                "Today" if i == 0
                else forecast_date.strftime("%a")
            )

            with col:

                card_html = dedent(f"""
                    <div class="forecast-card">
                        <div style="font-size:12px;color:#66809a;">
                            {day_name}
                        </div>
                        <div style="font-size:11px;color:#66809a;">
                            {forecast_date.strftime('%d %b')}
                        </div>
                        <div class="weather-icon">
                            {day_icon}
                        </div>
                        <div class="forecast-temp">
                            {daily['temperature_2m_max'][i]:.0f}°
                        </div>
                        <div style="font-size:11px;color:#66809a;">
                            Low {daily['temperature_2m_min'][i]:.0f}°
                        </div>
                        <div style="font-size:10px;color:#66809a;margin-top:8px;">
                            Rain {daily['precipitation_probability_max'][i]}%
                        </div>
                    </div>
                """)

                st.markdown(
                    card_html,
                    unsafe_allow_html=True
                )

    # Selected-date hourly graph

    st.markdown("### ⏰ Hourly Forecast for Selected Date")

    hourly_df = pd.DataFrame({
        "time": pd.to_datetime(hourly["time"]),
        "temperature": hourly["temperature_2m"],
        "rain": hourly["precipitation_probability"],
        "wind": hourly["wind_speed_10m"]
    })

    selected_hours = hourly_df[
        hourly_df["time"].dt.date == selected_date
    ]

    if not selected_hours.empty:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=selected_hours["time"],
            y=selected_hours["temperature"],
            mode="lines+markers",
            name="Temperature",
            line=dict(color="#2499dc", width=3)
        ))

        fig.update_layout(
            template="plotly_white",
            title="Temperature throughout the selected day",
            xaxis_title="Time",
            yaxis_title="Temperature °C",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            selected_hours.rename(columns={
                "time": "Time",
                "temperature": "Temperature °C",
                "rain": "Rain Probability %",
                "wind": "Wind Speed km/h"
            }),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Hourly forecast is not available for this date.")

    # Global cities

    st.markdown("### 🌍 Other Global Cities")

    global_cities = [
        ("Mumbai", 19.0760, 72.8777),
        ("London", 51.5072, -0.1276),
        ("Tokyo", 35.6762, 139.6503),
        ("New York", 40.7128, -74.0060),
        ("Dubai", 25.2048, 55.2708),
        ("Sydney", -33.8688, 151.2093)
    ]

    city_columns = st.columns(3)

    for i, (name, city_lat, city_lon) in enumerate(global_cities):

        try:

            other = get_weather(city_lat, city_lon)
            other_current = other["current"]

            other_icon, other_desc = weather_info(
                other_current["weather_code"]
            )

            with city_columns[i % 3]:

                st.markdown(f"""
                <div class="city-card">
                    <b>{name}</b>
                    <div style="font-size:28px;margin-top:7px;">
                        {other_icon}
                        <b>{other_current['temperature_2m']}°C</b>
                    </div>
                    <div style="font-size:12px;color:#66809a;">
                        {other_desc}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except requests.RequestException:
            continue

    # Map

    st.markdown("### 🗺️ Global Weather Map")

    map_locations = [
        {"name": city, "lat": lat, "lon": lon}
    ] + [
        {"name": n, "lat": a, "lon": b}
        for n, a, b in global_cities
        if n.casefold() != city.casefold()
    ]

    map_df = pd.DataFrame(map_locations)

    fig = go.Figure(go.Scattergeo(
        lon=map_df["lon"],
        lat=map_df["lat"],
        text=map_df["name"],
        mode="markers+text",
        textposition="top center",
        marker=dict(
            size=11,
            color="#2499dc",
            line=dict(color="white", width=2)
        ),
        hovertemplate="%{text}<extra></extra>"
    ))

    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="#d7e4ed",
        showocean=True,
        oceancolor="#eaf5fc",
        showcountries=True,
        countrycolor="white"
    )

    fig.update_layout(
        template="plotly_white",
        height=400,
        margin=dict(l=0, r=0, t=10, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Weather metrics

    st.markdown("### 🌡️ Current Weather Details")

    metrics = [
        ("Current Temperature", f"{current['temperature_2m']}°C"),
        ("Humidity", f"{current['relative_humidity_2m']}%"),
        ("Feels Like", f"{current['apparent_temperature']}°C"),
        ("Wind Speed", f"{current['wind_speed_10m']} km/h"),
        ("Pressure", f"{current['pressure_msl']} hPa"),
        ("Cloud Cover", f"{current['cloud_cover']}%")
    ]

    metric_cols = st.columns(3)

    for i, (label, value) in enumerate(metrics):
        metric_cols[i % 3].metric(label, value)


# =====================================================
# WEATHER ANALYTICS
# =====================================================

with tab2:

    st.markdown("## 📊 Weather Analytics")

    analytics_choice = st.selectbox(
        "Select analysis",
        ["Temperature", "Rain Probability", "Wind Speed", "Humidity"]
    )

    column_mapping = {
        "Temperature": ("temperature_2m", "Temperature °C", "#2499dc"),
        "Rain Probability": ("precipitation_probability", "Rain %", "#269bd5"),
        "Wind Speed": ("wind_speed_10m", "Wind km/h", "#20a879"),
        "Humidity": ("relative_humidity_2m", "Humidity %", "#8974dc")
    }

    key, label, color = column_mapping[analytics_choice]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hourly["time"][:48],
        y=hourly[key][:48],
        mode="lines+markers",
        line=dict(color=color, width=3),
        name=analytics_choice
    ))

    fig.update_layout(
        template="plotly_white",
        title=f"Next 48 Hours - {analytics_choice}",
        xaxis_title="Date and Time",
        yaxis_title=label,
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# AIR QUALITY
# =====================================================

with tab3:

    st.markdown("## 🌫️ Air Quality Monitoring")

    try:

        air_data = get_air(lat, lon)
        air = air_data.get("current", {})

        aqi = air.get("us_aqi")

        if aqi is None:

            st.warning("AQI data unavailable.")

        else:

            aqi = float(aqi)

            if aqi <= 50:
                status = "Good"
            elif aqi <= 100:
                status = "Moderate"
            elif aqi <= 150:
                status = "Unhealthy for Sensitive Groups"
            elif aqi <= 200:
                status = "Unhealthy"
            elif aqi <= 300:
                status = "Very Unhealthy"
            else:
                status = "Hazardous"

            st.metric("US Air Quality Index", f"{aqi:.0f}")
            st.subheader(status)

            a, b = st.columns(2)

            a.metric(
                "PM2.5",
                f"{air.get('pm2_5', 'N/A')} μg/m³"
            )

            b.metric(
                "PM10",
                f"{air.get('pm10', 'N/A')} μg/m³"
            )

    except requests.RequestException:
        st.warning("Air quality service is temporarily unavailable.")


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#66809a;padding:20px;">
        🌦️ WeatherVision AI
        <br>
        Global Weather Intelligence & Climate Analytics
        <br><br>
        Weather Data: Open-Meteo
    </div>
    """,
    unsafe_allow_html=True
)
