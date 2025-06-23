import argparse, time
from analysis import *
from util import *

datapath = os.path.join(os.getcwd(), "data")

def main(mode, filename=None):
    if mode == 'compare_algorithm':
        if not filename:
            print("Missing filepath for 'compare_algorithm' mode.")
            return
        filepath = os.path.join(datapath, "graphml", filename)
        G, positions = load_gposition_from_graphml(filepath)
        print("Finished loading graphml data")
        compare_bfs_dfs(G, positions)

    elif mode == 'normal_extract':
        if not filename:
            print("Missing filepath for 'normal_extract' mode.")
            return
        filepath = os.path.join(datapath, "graphml", filename)
        G, positions = load_gposition_from_graphml(filepath)
        print("Finished loading graphml data")

        start_time = time.time()
        patterns = extract_patterns(G, positions)
        end_time = time.time()
        print(f"Finished pattern extraction in {end_time - start_time}")

        nodes, branches = summarize_patterns(patterns)
        print(f" Nodes: {nodes}, Branches: {branches}")

    elif mode == 'plot_bfs':
        if not filename:
            print("Missing filepath for 'plot_bfs' mode.")
            return
        filepath = os.path.join(datapath, "graphml", filename)
        G, positions = load_gposition_from_graphml(filepath)
        print("Finished loading graphml data")
        
        start_time = time.time()
        patterns = bfs_extract_patterns(G, positions)
        end_time = time.time()
        print(f"Finished pattern extraction in {end_time - start_time}")

        nodes, branches = summarize_patterns(patterns)
        print(f"BFS - Nodes: {nodes}, Branches: {branches}")

        plot_patterns(patterns)

    elif mode == 'plot_dfs':
        if not filename:
            print("Missing filepath for 'plot_dfs' mode.")
            return
        filepath = os.path.join(datapath, "graphml", filename)
        G, positions = load_gposition_from_graphml(filepath)
        print("Finished loading graphml data")

        start_time = time.time()
        patterns = dfs_extract_patterns(G, positions)
        end_time = time.time()
        print(f"Finished pattern extraction in {end_time - start_time}")

        nodes, branches = summarize_patterns(patterns)
        print(f"DFS - Nodes: {nodes}, Branches: {branches}")
        plot_patterns(patterns)

    else:
        print("Invalid mode.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="L-System Tool CLI")
    parser.add_argument("mode", choices=["compare_algorithm", "normal_extract", "plot_dfs", "plot_bfs"],
                        help="Operation mode: 'compare_algorithm', 'normal_extract'.")
    parser.add_argument("filepath", nargs="?", default=None,
                        help="Optional filepath for 'compare_algorithm' mode.")

    args = parser.parse_args()
    main(args.mode, args.filepath)