import os
from analysis import *
from util import *
import threading

datapath = os.path.join(os.getcwd(), "data")

def clear_screen():
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For macOS and Linux
        _ = os.system('clear')

def print_files_in_directory(title, directory):
    """
    Print all files in the given directory, excluding '.gitkeep'.
    """
    if not os.path.isdir(directory):
        print(f"'{directory}' is not a valid directory.")
        return

    print(title)
    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path) and filename != ".gitkeep":
            print(f" - {filename}")

def file_exists_in_directory(directory, filename):
    """
    Check if a file with the given name exists in the specified directory.

    Returns True if the file exists, False otherwise.
    """
    full_path = os.path.join(directory, filename)
    return os.path.isfile(full_path)

def press_back():
    print("\033[92mPress anything to go back\033[0m")

def invalid_input():
    print("\033[91mInvalid input!\033[0m")

def main_menu():
    print("REAL CITY STREET L-SYSTEM GENERATOR")
    print("Created by: Aryo Wisanggeni (13523100) - Github: Staryo40")
    print("Main Menu Options:")
    print("1. Import geographical graphml")
    print("2. Create patterns with BFS/DFS using graphml data")
    print("3. Create L-System from patterns (must be saved to .json)")
    print("4. View graphml files")
    print("5. View patterns files")
    print("6. View numeric l-system files")
    print("7. View reference l-system files")
    print("8. Plot pattern")
    print("9. Plot l-system")
    print("10. Plot pattern vs numeric l-system")
    print("-----------------------------------------------------------")

    choice = -1
    start = True
    while choice < 0 and choice > 10:
        if start:
            start = False
        else:
            invalid_input()
        choice = int(input("Input your choice (1-9): "))
    
    return choice

def choose_algo():
    start = True
    print("USE BFS OR DFS?")
    print("1. BFS")
    print("2. DFS")
    print("3. Exit")
    while (algo_choice.lower() != "bfs" and int(algo_choice) != 1 and algo_choice.lower() != "dfs" and int(algo_choice) != 2 and algo_choice.lower() != "exit" and int(algo_choice) != 3):
        if (start):
            start = False
        else:
            invalid_input()
        algo_choice = input("Algo: ")

    return algo_choice

def lsystem_processing(patterns):
    while True:
        clear_screen()
        print("L-SYSTEM PROCESSING")
        print("Which type of L-System to produce?")
        print("1. Save numeric L-System (similar to actual geo shape)")
        print("2. Save reference L-System (for seeing trends in traditional L-System)")
        print("3. Exit")
        choice = int(input("Input (1-3): "))
        print()
        if (choice == 3):
            return
        if (choice != 1 and choice != 2):
            invalid_input()
            press_back()
            inp = input()
        break

    clear_screen()
    print("Generating L-Systems...")
    raw_rules = create_raw_rules(patterns)
    filtered_rules = filter_rules(raw_rules)
    split, gen_rules = generalize_rule(filtered_rules, original_id=True, split=True)
    filename = input("Input filename: ")
    if not filename.endswith(".json"):
        filename += ".json"

    if (choice == 1):
        path = os.path.join(datapath, "numeric_lsystem", filename)
        save_numeric_lsystem_to_json(filtered_rules, path)

        print("Successfully saved Numeric L-System")
        print(f"Produced rules: {len(filtered_rules)}")
        print(f"First 5 rules: ")
        for i, (id, rule) in enumerate(filtered_rules.items()):
            if i < 5:
                print(f"{id}: {rule}")
    elif (choice == 2):
        path = os.path.join(datapath, "numeric_lsystem", filename)
        save_referential_lsystem_to_json(split, gen_rules, path)

        print("Successfully saved Referential L-System")
        print(f"Produced rules: {len(gen_rules)}")
        print(f"Non-reference rules: {split[0]}")
        print(f"Reference rules: {split[1]}")
        print(f"First 5 nonreference rules: ")
        for i, (id, rule) in enumerate(gen_rules.items()):
            if i < 5:
                print(f"{id}: {rule}")
        print(f"First 5 reference rules: ")
        for i, (id, rule) in enumerate(gen_rules.items()):
            if i > split[0] and i < split[0] + 6:
                print(f"{id}: {rule}")
    press_back()
    inp = input()
            
def process_pattern():
    dir = os.path.join(datapath, "graphml")
    print("CREATE PATTERN WITH BFS/DFS")
    print_files_in_directory("Current graphml files:", dir)
    print("-----------------------------------------------------------")
    file = input("Enter the name of file to process pattern (exact): ")
    if file_exists_in_directory(dir, file):
        filepath = os.path.join(dir, file)
        clear_screen()

        algo_choice = choose_algo()

        clear_screen()
        if (algo_choice.lower() == "exit" or  int(algo_choice) == 3):
            return

        patterns = {}
        exec_time = 0
        if (algo_choice.lower() == "bfs" or  int(algo_choice) == 1):
            start_time = time.time()
            patterns = bfs_extract_patterns(filepath)
            end_time = time.time()
            exec_time = end_time - start_time
        elif (algo_choice.lower() == "dfs" or  int(algo_choice) == 2):
            start_time = time.time()
            patterns = dfs_extract_patterns(filepath)
            end_time = time.time()
            exec_time = end_time - start_time
        
        node, branch = summarize_patterns(patterns)

        print("PATTERN PROCESSED!")
        if (algo_choice.lower() == "bfs" or  int(algo_choice) == 1):
            print(f"Using BFS took {exec_time} seconds")
        elif (algo_choice.lower() == "dfs" or  int(algo_choice) == 2):
            print(f"Using DFS took {exec_time} seconds")
        print(f"Pattern - Node: {node}, Branch: {branch}")
        save = input("Save pattern as json (y/n)? ")
        print()
        if (save.lower() == "y"):
            name = input("Input file name: ")
            if not name.endswith(".json"):
                name += ".json"
            filepath = os.path.join(datapath, "pattern", name)
            save_patterns_to_json(patterns, filepath)
            print("Successfully saved file!")
        press_back()
        inp = input()
    else:
        print(f"File {file} does not exist!")
        press_back()
        inp = input()
    clear_screen()

def process_lsystem():
    dir = os.path.join(datapath, "pattern")
    print("PROCESS L-SYSTEM WITH EXTRACTED PATTERN")
    print_files_in_directory("Current pattern files:", dir)
    print("-----------------------------------------------------------")
    file = input("Enter the name of file to process (exact): ")
    if file_exists_in_directory(dir, file):
        filepath = os.path.join(dir, file)
        clear_screen()

        patterns = load_patterns_from_json(filepath)
        lsystem_processing(patterns)
    else:
        print(f"File {file} does not exist!")
        press_back()
        inp = input()
    clear_screen()

def plot_pattern_main():
    dir = os.path.join(datapath, "pattern")
    print("PLOT PATTERN")
    print_files_in_directory("Current pattern files:", dir)
    print("-----------------------------------------------------------")
    file = input("Enter the name of file to process (exact): ")
    print()
    if file_exists_in_directory(dir, file):
        path = os.path.join(dir, file)
        patterns = load_patterns_from_json(path)
        print("Plotting pattern...")
        t = threading.Thread(target=plot_patterns, args=(patterns,))
        t.start()

        press_back()
        input()
    else:
        print(f"File {file} does not exist!")
        press_back()
        inp = input()

def plot_lsystem_main():
    choice = 1
    while True:
        clear_screen()
        print("L-SYSTEM PLOTTING")
        print("Which type of L-System to plot?")
        print("1. Numeric L-System (similar to actual geo shape)")
        print("2. Reference L-System (for seeing trends in traditional L-System)")
        print("3. Exit")
        choice = int(input("Input (1-3): "))
        print()
        if (choice == 3):
            return
        if (choice != 1 and choice != 2):
            invalid_input()
            press_back()
            inp = input()
        break
    
    dir = os.path.join(datapath, "pattern")
    print("PLOT L-SYSTEM")
    print_files_in_directory("Current pattern files:", dir)
    print("-----------------------------------------------------------")
    file = input("Enter the name of file to process (exact): ")
    print()
    if file_exists_in_directory(dir, file):
        path = os.path.join(dir, file)
        patterns = load_patterns_from_json(path)
        raw_rules = create_raw_rules(patterns)
        filtered_rules = filter_rules(raw_rules)
        split, gen_rules = generalize_rule(filtered_rules, original_id=True, split=True)
        print("Plotting l-system...")
        if (choice == 1):
            t = threading.Thread(target=draw_numeric_lsystem, args=(filtered_rules, patterns))
            t.start()
        elif (choice == 2):
            t = threading.Thread(target=draw_virtual_lsystem, args=(gen_rules, split))
            t.start()
    else:
        print(f"File {file} does not exist!")

    press_back()
    inp = input()

def plot_pattern_lsystem_main():
    dir = os.path.join(datapath, "pattern")
    print("PLOT L-SYSTEM vs PATTERN")
    print_files_in_directory("Current pattern files:", dir)
    print("-----------------------------------------------------------")
    file = input("Enter the name of file to process (exact): ")
    print()
    if file_exists_in_directory(dir, file):
        path = os.path.join(dir, file)
        patterns = load_patterns_from_json(path)
        raw_rules = create_raw_rules(patterns)
        filtered_rules = filter_rules(raw_rules)

        print("Plotting l-system and pattern...")
        t = threading.Thread(target=draw_pattern_and_numeric_lsystem, args=(patterns, filtered_rules))
        t.start()
    else:
        print(f"File {file} does not exist!")

    press_back()
    inp = input()

def download_geo_graphml_main():
    dir = os.path.join(datapath, "graphml")
    print("DOWNLOADING REAL GEOGRAPHICAL STREETS")
    print("📍 Please enter a location in a format like:")
    print("   - 'Bandung, Indonesia'")
    print("   - 'New York City, New York, USA'")
    print("   - 'Tokyo, Japan'")
    print("🛈 The more specific the location, the more accurate the result.\n")
    loc = input("Input location: ")
    filename = loc.split(",")[0].strip().replace(" ", "_") + ".graphml"

    print("This might take a while (a few minutes)")
    print("Downloading...")

    try:
        download_street_graphml(loc, dir, filename)
        print("Download successful")
    except Exception as e:
        print(f"\033[91m Failed to download: {e}\033[0m")

    press_back()
    input()

if __name__ == "__main__":
    while True:
        clear_screen()
        choice = main_menu()

        if choice == 1:
            clear_screen()
            download_geo_graphml_main()
        elif choice == 2:
            clear_screen()
            process_pattern()
        elif choice == 3:
            clear_screen()
            process_lsystem()
        elif choice == 4:
            dir = os.path.join(datapath, "graphml")
            clear_screen()
            print_files_in_directory("Saved graphml files: ", dir)
            press_back()
            inp = input()
        elif choice == 5:
            dir = os.path.join(datapath, "pattern")
            clear_screen()
            print_files_in_directory("Saved pattern files: ", dir)
            press_back()
            inp = input()
        elif choice == 6:
            dir = os.path.join(datapath, "numeric_lsystem")
            clear_screen()
            print_files_in_directory("Saved numeric l-system files: ", dir)
            press_back()
            inp = input()
        elif choice == 7:
            dir = os.path.join(datapath, "reference_lsystem")
            clear_screen()
            print_files_in_directory("Saved reference l-system files: ", dir)
            press_back()
            inp = input()
        elif choice == 8:
            clear_screen()
            plot_pattern_main()
        elif choice == 9:
            clear_screen()
            plot_lsystem_main()
        elif choice == 10:
            clear_screen()
            plot_pattern_lsystem_main()
        



            

        


    
