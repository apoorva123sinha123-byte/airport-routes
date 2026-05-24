import plotly.graph_objects as go
from airport_route_decider import route_decider
import pandas as pd

all_airports = pd.read_csv("airports_updated.csv")
all_codes = all_airports["iata_code"].tolist()
all_names = all_airports["name"].tolist()
all_lats = all_airports["latitude_deg"].tolist()
all_lons = all_airports["longitude_deg"].tolist()

while True:
    start = input("\nEnter starting airport code (or 'quit' to exit): ").upper()
    if start == 'QUIT':
        break
    end = input("Enter ending airport code: ").upper()
    weighting = input("Shortest route possible or fewest layovers (S/F): ").upper()

    try:
        route = route_decider(start, end,weighting)[0]
        route_indices = [all_codes.index(i) for i in route]
    except:
        print("No route found. Please try again.")
        continue

    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        lon=all_lons,
        lat=all_lats,
        customdata=all_codes,
        mode='markers',
        text=all_names,
        marker=dict(size=6, color='black'),
        hovertemplate="<b>%{text}</b><br>IATA: %{customdata}<br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>",
        name="Airports"
    ))
    longitudes = [all_lons[i] for i in route_indices]
    latitudes = [all_lats[i] for i in route_indices]

    fig.add_trace(go.Scattergeo(
        lon=longitudes,
        lat=latitudes,
        mode='lines+markers',
        line=dict(width=3, color='red'),
        name="Optimized Route",
        hoverinfo="skip",
        showlegend=False
    ))

    fig.update_geos(
        projection_type='natural earth',
        projection_scale=1,
        showcountries=True,
        showland=True,
        landcolor='rgb(243, 243, 243)',
        center=dict(lat=latitudes[0], lon=longitudes[0])
    )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    fig.show()