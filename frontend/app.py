import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests
from PIL import Image
import io
import os

print(os.getcwd())
print(os.listdir(os.getcwd()))
file_path = os.path.join(os.path.dirname(__file__), "station_metadata.txt")

map_data = pd.read_csv(file_path, sep="\t")
filtered_map_data = map_data.dropna(subset=['Latitude', 'Longitude'])

st.title('Los Angeles Traffic Prediction')
st.subheader('Select a station to forecast traffic')

# only display filtered stations 
# read the station metadata file
with open('../notebooks/filtered_reduced_stations.txt', 'r') as f:
    filtered_stations = [int(line.replace('\n', '')) for line in f.readlines()]

# print(len(filtered_stations)) 344 stations

# filter the map data to only include stations in filtered_stations
filtered_map_data = filtered_map_data[filtered_map_data['ID'].isin(filtered_stations)]

m = folium.Map(location=[34.06, -118.27], zoom_start=9)

# # Add markers to the map
# for _, row in filtered_map_data.iterrows():
#     folium.Marker(
#         location=[row['Latitude'], row['Longitude']],
#         popup=str(row['ID']),  # Set station_id as popup
#         tooltip=row['Name']  # Show name on hover instead
#     ).add_to(m)

# # Display map and capture interaction
# output = st_folium(m, width=700, height=500)

# # Get clicked station ID from popup
# clicked_station_id = output.get("last_object_clicked_popup")

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
    st.session_state['selected_station_id'] = filtered_map_data[filtered_map_data['Name'] == clicked_station].iloc[0]['ID']
    print(st.session_state['selected_station_id'])

# print(filtered_map_data[filtered_map_data['Name'] == clicked_station].iloc[0]['ID'])


# Show prediction button if a station is selected
# also show options for number of periods and frequency
if 'selected_station' in st.session_state:
    station = st.session_state['selected_station']
    station_id = st.session_state['selected_station_id']
    st.write(f" You selected station **{station}**")

    selected_frequency = st.radio(
    "Select frequency",
    ["Hours", "Days"],
    )
    freq = None

    if selected_frequency == "Hours":
        freq = "h"
    elif selected_frequency == "Days":
        freq = "d"

    num_periods = st.number_input(  
        "Number of periods to predict",
        min_value=1,
        max_value=100,
        value=24,  # Default value
        step=1
    )
    if st.button(f"Predict for station {station}?"):
        st.success(f" Prediction triggered for station {station}")
        url = "https://traffic-prediction-los-angeles-418-26302743692.europe-west1.run.app/forecast-traffic"  
        payload = {
            "station_id": str(station_id),
            "freq": freq,
            "periods": int(num_periods)
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                st.success(f"Prediction complete for station {station}")
                img_res = requests.get("https://traffic-prediction-los-angeles-418-26302743692.europe-west1.run.app/get-prophet-image")
                img = Image.open(io.BytesIO(img_res.content))
                st.image(img, caption="NeuralProphet Forecast Components for Average Speed over Time", 
                         use_container_width=True)
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")

