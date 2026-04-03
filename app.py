import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

# 1. Wetter-Funktion (Nutzt Open-Meteo, Key-frei)
def get_weather(city, days):
    try:
        geolocator = Nominatim(user_agent="reise_app_2026")
        location = geolocator.geocode(city)
        if not location:
            return None
        
        lat, lon = location.latitude, location.longitude
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum&timezone=auto"
        res = requests.get(url).json()
        
        df = pd.DataFrame({
            "Datum": res["daily"]["time"][:days],
            "Max Temp": res["daily"]["temperature_2m_max"][:days],
            "Regen (mm)": res["daily"]["precipitation_sum"][:days]
        })
        return df
    except:
        return None

# --- UI Setup ---
st.set_page_config(page_title="Free Travel Guide", layout="wide")
st.title("✈️ Reiseplaner (Ohne API-Key)")

# Sidebar
with st.sidebar:
    stadt = st.text_input("Stadt eingeben", "Paris")
    dauer = st.slider("Aufenthaltsdauer (Tage)", 1, 7, 3)
    suche = st.button("Reise planen")

if suche:
    st.header(f"Dein Trip nach {stadt}")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("☀️ Wetterprognose")
        wetter_data = get_weather(stadt, dauer)
        if wetter_data is not None:
            st.dataframe(wetter_data, use_container_width=True)
        else:
            st.warning("Wetterdaten konnten nicht geladen werden.")

    with col2:
        st.subheader("📍 Sehenswürdigkeiten & Kultur")
        # Da wir keinen Key haben, generieren wir hilfreiche Such-Links
        st.write(f"Hier sind die Highlights für {stadt}:")
        st.markdown(f"- [Top Attraktionen auf TripAdvisor](https://www.tripadvisor.de/Search?q={stadt})")
        st.markdown(f"- [Kulturelle Highlights (Wikipedia)](https://de.wikipedia.org/wiki/{stadt}#Kultur_und_Sehenswürdigkeiten)")
        
    st.divider()

    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🍴 Restaurants & Food")
        st.write("Empfohlene Suche:")
        st.info(f"Suche direkt bei [Yelp für {stadt}](https://www.yelp.de/search?find_desc=Restaurants&find_loc={stadt})")
        st.write("💡 *Tipp: Achte auf Orte mit mehr als 4 Sternen und lokalen Spezialitäten.*")

    with col4:
        st.subheader("📅 Veranstaltungen")
        st.write(f"Events während deines Aufenthalts:")
        st.markdown(f"- [Veranstaltungskalender {stadt}](https://www.google.com/search?q=events+{stadt}+next+days)")
        st.caption("Klicke auf den Link, um aktuelle Konzerte und Ausstellungen zu sehen.")

    # Karte anzeigen
    st.subheader("🗺️ Stadtplan")
    geolocator = Nominatim(user_agent="reise_app_2026")
    loc = geolocator.geocode(stadt)
    if loc:
        map_data = pd.DataFrame({'lat': [loc.latitude], 'lon': [loc.longitude]})
        st.map(map_data)
