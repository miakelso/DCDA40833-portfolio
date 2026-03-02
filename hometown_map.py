import requests
import pandas as pd
import folium
from urllib.parse import quote

# ==============================
# 1. ADD YOUR MAPBOX INFORMATION
# ==============================

MAPBOX_USERNAME = "miak26"
MAPBOX_STYLE_ID = "cmm0speuh005b01sc3xts6luv"
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoibWlhazI2IiwiYSI6ImNtbHRtdTk5bzAxd2MzZnB0b2doaXRtdmoifQ.LxKMkAV6CVbT15G6dFaQwg"

# Custom Mapbox tile URL
tiles = f"https://api.mapbox.com/styles/v1/{MAPBOX_USERNAME}/{MAPBOX_STYLE_ID}/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={MAPBOX_ACCESS_TOKEN}"

# ==============================
# 2. READ CSV FILE
# ==============================

df = pd.read_csv("hometown_locations.csv")

# ==============================
# 3. FUNCTION TO GEOCODE ADDRESS
# ==============================

def geocode_address(address):
    encoded_address = quote(address)
    geocode_url = f"https://api.mapbox.com/search/geocode/v6/forward?q={encoded_address}&access_token={MAPBOX_ACCESS_TOKEN}"
    
    response = requests.get(geocode_url)
    data = response.json()
    
    if data["features"]:
        coordinates = data["features"][0]["geometry"]["coordinates"]
        return coordinates[1], coordinates[0]  # Return lat, lon
    else:
        return None, None

# ==============================
# 4. CREATE BASE MAP
# ==============================

# Start map centered on Mansfield, TX area
base_map = folium.Map(
    location=[32.5632, -97.1417],
    zoom_start=11,
    tiles=tiles,
    attr="Mapbox"
)

# ==============================
# 5. ICON COLORS BY TYPE
# ==============================

type_colors = {
    "restaurant": "red",
    "park": "green",
    "cultural site": "blue",
    "school": "purple",
    "other": "gray"
}

# ==============================
# 6. ADD MARKERS
# ==============================

for index, row in df.iterrows():
    lat, lon = geocode_address(row["address"])
    
    if lat and lon:
        
        # Determine icon color
        location_type = row["type"].lower()
        color = type_colors.get(location_type, "gray")
        
        # Create HTML popup
        popup_html = f"""
        <div style="font-family: Arial, sans-serif;">
            <h4 style="margin: 0 0 10px 0;">{row['name']}</h4>
            <p style="margin: 0 0 10px 0;">{row['description']}</p>
            <img src="{row['image_url']}" width="200" style="border-radius: 5px;">
        </div>
        """
        
        iframe = folium.IFrame(popup_html, width=250, height=300)
        popup = folium.Popup(iframe, max_width=300)
        
        # Add marker
        folium.Marker(
            location=[lat, lon],
            popup=popup,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(base_map)

# ==============================
# 7. SAVE MAP
# ==============================

base_map.save("hometown_map.html")

print("Map has been saved as hometown_map.html")