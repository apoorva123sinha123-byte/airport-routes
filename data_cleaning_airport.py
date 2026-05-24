import pandas as pd

df1 = pd.read_csv("airports.txt", header=None, names=[
    'id', 'name', 'municipality', 'country_name',
    'iata_code', 'icao_code', 'latitude_deg', 'longitude_deg',
    'elevation_ft', 'utc_offset', 'dst', 'timezone',
    'type', 'source'
])

columns_to_remove1 = ['municipality', 'country_name', 'utc_offset',
                      'dst', 'timezone', 'type', 'source']

df1 = df1.drop(columns=columns_to_remove1)
df1 = df1.dropna(subset=['iata_code'])
df1 = df1[df1['iata_code'] != '\\N']
df1_IATA_code = df1["iata_code"].tolist()

df2 = pd.read_csv('routes.txt', header=None,
                   names=['airline', 'airline_id', 'source_airport', 'source_id',
                          'destination_airport', 'destination_id', 'codeshare', 'stops', 'equipment'])

columns_to_remove2 = ["airline", "airline_id", "source_id", "destination_id",
                      "codeshare", "equipment"]

df2 = df2.drop(columns=columns_to_remove2)

df2 = df2[df2["stops"] == 0]

df2 = df2.drop(columns = "stops")

df2_tuples = []
for index, row in df2.iterrows():
    if row["source_airport"] in df1_IATA_code and row["destination_airport"] in df1_IATA_code:
        df2_tuples.append((row["source_airport"], row["destination_airport"]))
        df2_tuples.append((row["destination_airport"], row["source_airport"]))

df2_tuples = list(set(df2_tuples))

df2_2 = pd.DataFrame(df2_tuples, columns=['source_airport', 'destination_airport'])

airports_df2 = list(set(df2_2["source_airport"]) & set(df2_2["destination_airport"]))

df1_list = []
for index, row in df1.iterrows():
    if row["iata_code"] in airports_df2:
        df1_list.append(row)

df1_2 = pd.DataFrame(df1_list).reset_index(drop=True)

df1_2.to_csv("airports_updated.csv", index=False)
df2_2.to_csv("routes_updated.csv", index=False)