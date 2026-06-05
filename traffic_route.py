import streamlit as st
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
import requests
import polyline
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setup
geolocator = Nominatim(user_agent="traffic_route_planner")
st.set_page_config(page_title="Smart Traffic Route Planner", page_icon="🌍", layout="wide")
st.title("🌍 Smart Traffic Route Planner")

# Region selection
region = st.selectbox("Choose your region", ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Kolkata"])

# Time input
col1, col2 = st.columns(2)
with col1:
    selected_hour = st.slider("Select hour", 0, 23, 9)
with col2:
    selected_day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

# Locations
current_loc = st.text_input("Your current location")
destination = st.text_input("Destination")

# Congestion prediction from R API
def get_congestion_prediction(day, hour):
    """Get congestion prediction from R plumber API."""
    try:
        res = requests.get("http://localhost:8000/predict", params={"day": day, "hour": hour}, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return float(data.get("prediction", 0))
        return None
    except (requests.ConnectionError, requests.Timeout, ValueError, KeyError):
        return None

# Route drawing
if st.button("Find Route"):
    if not current_loc or not destination:
        st.warning("Please enter both origin and destination.")
    else:
        try:
            origin = geolocator.geocode(current_loc, timeout=10)
            dest = geolocator.geocode(destination, timeout=10)
        except Exception as e:
            st.error(f"Geocoding error: {e}")
            origin, dest = None, None

        if origin and dest:
            m = folium.Map(location=[origin.latitude, origin.longitude], zoom_start=12)
            folium.Marker([origin.latitude, origin.longitude], tooltip="Start", icon=folium.Icon(color='green')).add_to(m)
            folium.Marker([dest.latitude, dest.longitude], tooltip="End", icon=folium.Icon(color='red')).add_to(m)

            # Get route from OSRM
            try:
                url = f"http://router.project-osrm.org/route/v1/driving/{origin.longitude},{origin.latitude};{dest.longitude},{dest.latitude}?overview=full"
                data = requests.get(url, timeout=10).json()

                if data.get('code') == 'Ok':
                    coords = polyline.decode(data['routes'][0]['geometry'])
                    folium.PolyLine(coords, color="blue", weight=6).add_to(m)
                    st.subheader("Route Map")
                    folium_static(m)

                    # Traffic prediction
                    congestion = get_congestion_prediction(selected_day, selected_hour)
                    if congestion is not None:
                        if congestion >= 70:
                            status = ("High Congestion 🚧", "red")
                        elif congestion >= 40:
                            status = ("Moderate Congestion ⚠", "orange")
                        else:
                            status = ("Low Congestion ✅", "green")

                        st.markdown(f"""
                            <div style='background-color:{status[1]};padding:10px;border-radius:5px;color:white;'>
                            <b>Predicted Traffic:</b> {congestion:.1f}%<br>
                            <b>Status:</b> {status[0]}</div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("Traffic prediction API unavailable. Route displayed without congestion data.")
                else:
                    st.error("Routing failed — OSRM could not find a route.")
            except requests.Timeout:
                st.error("Routing request timed out. Please try again.")
            except Exception as e:
                st.error(f"Routing error: {e}")
        elif origin is None:
            st.error(f"Could not find location: '{current_loc}'")
        elif dest is None:
            st.error(f"Could not find location: '{destination}'")

# EDA option
if st.checkbox("Show EDA from Model Data"):
    try:
        eda_data = pd.read_csv("http://localhost:8000/eda")
        st.subheader("Traffic Pattern Overview")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=eda_data, x="Hour", y="Congestion", hue="Day", ax=ax)
        st.pyplot(fig)
        plt.close(fig)
    except requests.ConnectionError:
        st.warning("Could not connect to EDA API. Make sure the R plumber API is running.")
    except Exception as e:
        st.warning(f"Could not load EDA data: {e}")
