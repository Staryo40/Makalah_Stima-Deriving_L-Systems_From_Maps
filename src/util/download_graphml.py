import osmnx as ox
import os
import matplotlib.pyplot as plt

def download_street_graphml(geo_name, datapath, filename):
    if not filename.endswith(".graphml"):
        filename += ".graphml"

    G = ox.graph_from_place(geo_name, network_type="drive")

    downloadpath = os.path.join(datapath, filename)
    ox.save_graphml(G, downloadpath)

if __name__ == '__ main __':
    ox.settings.log_console = True
    ox.settings.use_cache = True

    G = ox.graph_from_place("New York City, New York, USA", network_type="drive")
    # G = ox.graph_from_place("Bandung, Indonesia", network_type="drive")
    # G = ox.graph_from_place("Jakarta, Indonesia", network_type="drive")
    ox.save_graphml(G, "new-york.graphml")
