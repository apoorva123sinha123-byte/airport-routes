import pandas as pd
import math

def harversine_formula(ln1, lt1, ln2, lt2):
    R = 6371.0
    phi1, phi2 = math.radians(lt1), math.radians(lt2)
    dphi = math.radians(lt2 - lt1)
    dlambda = math.radians(ln2 - ln1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_airport_coords(iata_code):
    lat = airport_df.loc[iata_code, 'latitude_deg']
    lon = airport_df.loc[iata_code, 'longitude_deg']
    return lat, lon

route_df = pd.read_csv("routes_updated.csv")

start_airport = route_df["source_airport"].tolist()
end_airport = route_df["destination_airport"].tolist()

airport_df = pd.read_csv("airports_updated.csv")
columns_to_remove_airports = ["id","name","elevation_ft","icao_code"]
airport_df = airport_df.drop(columns=columns_to_remove_airports)
airport_df = airport_df.set_index('iata_code')

airport_routes = {}


index = 0
while index < len(start_airport):
    lat1,lon1 = get_airport_coords(start_airport[index])
    lat2,lon2 = get_airport_coords(end_airport[index])
    if start_airport[index] not in airport_routes.keys():
        airport_routes[start_airport[index]] = f"({end_airport[index]}|{harversine_formula(lon1,lat1,lon2,lat2)})"
    elif start_airport[index] in airport_routes.keys():
        airport_routes[start_airport[index]] += f"+({end_airport[index]}|{harversine_formula(lon1,lat1,lon2,lat2)})"
    index += 1

out_df = pd.DataFrame.from_dict(airport_routes,orient="index")

out_df.to_csv("routes_updated_2.csv")

