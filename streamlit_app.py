# streamlit_app.py
import streamlit as st
import pandas as pd
import requests
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static

st.set_page_config(page_title="Smart Traffic Planner", layout="wide")
st.title("🚦 Smart Traffic Route Planner")

# Inputs
region = st.selectbox("Region", ["Delhi", "Mumbai", "Bangalore"])
day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
hour = st.slider("Hour of Day", 0, 23, 9)
origin = st.text_input("Current Location", "Connaught Place, Delhi")
destination = st.text_input("Destination", "Indira Gandhi Airport, Delhi")

# Congestion prediction from R backend API
def get_congestion_prediction(day, hour):
    """Fetch congestion prediction from R plumber API."""
    try:
        res = requests.post("http://localhost:8000/predict", json={"day": day, "hour": hour}, timeout=5)
        if res.status_code == 200:
            return res.json().get("congestion", None)
        return None
    except (requests.ConnectionError, requests.Timeout):
        return None

if st.button("Get Best Route"):
    st.subheader("📍 Mapping Route and Congestion Prediction")

    geolocator = Nominatim(user_agent="smart_traffic_planner")

    try:
        loc1 = geolocator.geocode(origin, timeout=10)
        loc2 = geolocator.geocode(destination, timeout=10)
    except Exception as e:
        st.error(f"Geocoding error: {e}")
        loc1, loc2 = None, None

    if loc1 and loc2:
        map_center = [loc1.latitude, loc1.longitude]
        m = folium.Map(location=map_center, zoom_start=12)
        folium.Marker([loc1.latitude, loc1.longitude], tooltip="Start", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker([loc2.latitude, loc2.longitude], tooltip="End", icon=folium.Icon(color="red")).add_to(m)

        congestion = get_congestion_prediction(day, hour)

        # Distance and time estimation
        distance_km = ((loc1.latitude - loc2.latitude)**2 + (loc1.longitude - loc2.longitude)**2) ** 0.5 * 111
        base_time_min = distance_km / 40 * 60

        if congestion is not None:
            est_time = base_time_min * (1 + congestion / 100)
        else:
            est_time = base_time_min

        folium.PolyLine([[loc1.latitude, loc1.longitude], [loc2.latitude, loc2.longitude]], color="blue").add_to(m)
        folium_static(m)

        col1, col2 = st.columns(2)
        if congestion is not None:
            col1.metric("Estimated Congestion", f"{congestion:.1f}%")
        else:
            col1.warning("R model API unavailable — showing base estimate.")
        col2.metric("Estimated Travel Time", f"{est_time:.1f} min")
    else:
        st.error("Could not geocode one or both locations. Please check your inputs.")

st.markdown("---")
st.subheader("📊 Traffic Trends")

if st.checkbox("Show Traffic Trends"):
    try:
        df = pd.read_csv("api_traffic_data.csv")
        st.line_chart(df.groupby("Hour")["Congestion"].mean())
        st.bar_chart(df.groupby("Day")["Congestion"].mean())
    except FileNotFoundError:
        st.warning("Traffic data file `api_traffic_data.csv` not found.")
    except Exception as e:
        st.error(f"Error loading traffic data: {e}")
