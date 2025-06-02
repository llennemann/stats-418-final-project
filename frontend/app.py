import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests


map_data = pd.read_csv("station_metadata.txt", sep="\t")
# null_stations = [x for x in map_data['ID'] if map_data['Latitude'].isna() | map_data['Longitude'].isna()]
filtered_map_data = map_data.dropna(subset=['Latitude', 'Longitude'])

st.title('Los Angeles traffic prediction')
st.subheader('Select a station to forecast traffic')

# only display filtered stations 
# read the station metadata file
with open('../notebooks/filtered_stations.txt', 'r') as f:
    filtered_stations = [int(line.replace('\n', '')) for line in f.readlines()]

# filter the map data to only include stations in filtered_stations
filtered_map_data = filtered_map_data[filtered_map_data['ID'].isin(filtered_stations)]

m = folium.Map(location=[34.06, -118.27], zoom_start=9)

# Add markers to the map
for _, row in filtered_map_data.iterrows():
    if row['ID'] in filtered_stations:
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['Name'],
            # tooltip=f"Station {row['station_id']}"
        ).add_to(m)

# Display map and capture interaction
output = st_folium(m, width=700, height=500)

# Check for clicked marker (popup)
clicked_station = output.get("last_object_clicked_popup")

if clicked_station:
    st.session_state['selected_station'] = clicked_station

# Show prediction button if a station is selected
# also show options for number of periods and frequency
if 'selected_station' in st.session_state:
    station = st.session_state['selected_station']
    st.write(f" You selected station **{station}**")

    selected_frequency = st.radio(
    "Select frequency",
    ["Hours", "Days"],
    )
    if st.button(f"Predict for station {station}?"):
        st.success(f" Prediction triggered for station {station}")
        # url = "http://localhost:5001/forecast-traffic"  # Update if running elsewhere
        # payload = {
        #     "station_id": station,
        #     "freq": "h"  
        # }

        # try:
        #     response = requests.post(url, json=payload)
        #     if response.status_code == 200:
        #         st.success(f"Prediction complete for station {station}")
        #         # Optionally display returned data
        #         result = response.json()
        #         st.json(result)
        #     else:
        #         st.error(f"API Error: {response.status_code} - {response.text}")
        # except requests.exceptions.RequestException as e:
        #     st.error(f"Connection error: {e}")

