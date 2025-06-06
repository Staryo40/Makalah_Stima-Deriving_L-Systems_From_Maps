import osmnx as ox
import matplotlib.pyplot as plt

ox.settings.log_console = True
ox.settings.use_cache = True

G = ox.graph_from_place("New York City, New York, USA", network_type="drive")
# G = ox.graph_from_place("Bandung, Indonesia", network_type="drive")
# G = ox.graph_from_place("Jakarta, Indonesia", network_type="drive")
ox.save_graphml(G, "new-york.graphml")

# ox.plot_graph(G, bgcolor="white", node_color="red", edge_color="gray")

# nodes, edges = ox.graph_to_gdfs(G)
# edges.to_file("jakarta.gpkg", driver="GPKG")
