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
        # patterns = extract_patterns(G, positions)
        # patterns = bfs_extract_patterns(G, positions)
        patterns = optimized_extract_patterns(G, positions)
        end_time = time.time()
        print(f"Finished pattern extraction in {end_time - start_time}")

        nodes, branches = summarize_patterns(patterns)
        print(f" Nodes: {nodes}, Branches: {branches}")

        save_patterns_to_json(patterns, "bandung_bfs.json")

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

    elif mode == 'plot_num_lsystem':
        if not filename:
            print("Missing filepath for 'plot_num_lsystem' mode.")
            return
        
        filepath = os.path.join(datapath, "pattern", filename)
        patterns = load_patterns_from_json(filepath)
        raw_rules = create_raw_rules(patterns)
        filtered_rules = filter_rules(raw_rules)
        
        draw_numeric_lsystem(filtered_rules, patterns)

    elif mode == "plot_ref_lsystem":
        if not filename:
            print("Missing filepath for 'plot_ref_lsystem' mode.")
            return
        
        filepath = os.path.join(datapath, "pattern", filename)
        patterns = load_patterns_from_json(filepath)
        raw_rules = create_raw_rules(patterns)
        filtered_rules = filter_rules(raw_rules)
        split, gen_rules = generalize_rule(filtered_rules, original_id=True, split=True)

        draw_virtual_lsystem(gen_rules, split)

    else:
        print("Invalid mode.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="L-System Tool CLI")
    parser.add_argument("mode", choices=["compare_algorithm", "normal_extract", "plot_dfs", "plot_bfs", "plot_ref_lsystem", "plot_num_lsystem"],
                        help="Operation mode: 'compare_algorithm', 'normal_extract'.")
    parser.add_argument("filepath", nargs="?", default=None,
                        help="Optional filepath for 'compare_algorithm' mode.")

    args = parser.parse_args()
    main(args.mode, args.filepath)