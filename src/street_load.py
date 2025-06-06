import osmnx as ox
import matplotlib.pyplot as plt
import os, time

start = time.time()
path = os.path.join(os.getcwd(), "data", "bandung.graphml")
G = ox.load_graphml(path)  
end = time.time()

print(f"Load time: {end-start}")
# Bandung: 5 seconds
# New York: 14 seconds
# Jakarta: 20 seconds
fig, ax = ox.plot_graph(G, figsize=(10, 10))

plt.show()