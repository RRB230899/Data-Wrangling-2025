import requests
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Define API parameters
base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

params = {
    "format": "geojson",
    "starttime": "2020-01-01",
    "endtime": "2025-04-26",
    "minmagnitude": 5.5,
    "maxlatitude": 25.5,
    "minlatitude": 21.5,
    "maxlongitude": 122,
    "minlongitude": 119,
}

# Send GET request
response = requests.get(base_url, params=params)

# Check if successful
if response.status_code == 200:
    data = response.json()
    # Flatten the JSON structure
    earthquakes = []
    for feature in data['features']:
        prop = feature['properties']
        earthquakes.append({
            "time": pd.to_datetime(prop['time'], unit='ms'),
            "place": prop['place'],
            "magnitude": prop['mag'],
            "depth": feature['geometry']['coordinates'][2],  # Depth is 3rd element
            "latitude": feature['geometry']['coordinates'][1],
            "longitude": feature['geometry']['coordinates'][0]
        })

    # Create DataFrame
    eq_df = pd.DataFrame(earthquakes)
    print(eq_df)
    eq_df.to_csv('taiwan_earthquake_data_2020_to_2025.csv', index=False)
else:
    print(f"Failed to retrieve data: {response.status_code}")
