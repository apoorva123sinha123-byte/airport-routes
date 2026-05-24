import pandas as pd
import networkx as nx

def route_decider(source,target,weightage):
    distance = 0
    df = pd.read_csv("routes_updated_2.csv")

    airports = df["Unnamed: 0"].tolist()
    destinations_raw = df["0"].tolist()
    destinations = {}

    index = 0
    for i in destinations_raw:
        list_form = i.split("+")
        destinations[airports[index]] = {}
        for j in list_form:
            clean_j = j.replace("(", "").replace(")","")
            destination, weight = clean_j.split("|")
            destinations[airports[index]][destination] = float(weight)
        index += 1

    G = nx.DiGraph()

    for origin, routes in destinations.items():
        for dest, distance in routes.items():
            G.add_edge(origin, dest, weight=float(distance))

    try:

        if weightage == "S":
            path = nx.shortest_path(G, source=source, target=target, weight='weight')
            distance = nx.shortest_path_length(G, source=source, target=target, weight='weight')

        else:
            path = nx.shortest_path(G, source=source, target=target)
            distance = 0
            for i in range(len(path) - 1):
                edge_data = G.get_edge_data(path[i], path[i + 1])
                distance += edge_data['weight']


        print(f"Shortest path from {source} to {target}: {path}")

        print(f"Total distance: {distance:.2f} km")

        return [path, distance]

    except nx.NetworkXNoPath:
        print(f"No flight route exists between {source} and {target}.")

        return None