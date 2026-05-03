import csv
import sys
from collections import deque

# -------------------------------------------------------
# DATA STRUCTURES
# -------------------------------------------------------

city_name_to_ids = {}

# Maps city_id -> { "name": ..., "country": ..., "flights": set of (flight_id, dest_city_id) }
cities = {}

airlines = {}


# -------------------------------------------------------
# LOAD DATA FROM CSV FILES
# -------------------------------------------------------

def load_data(directory):
    """
    Load cities, flights, and airlines data from CSV files
    located in the given directory.
    """

    with open(f"{directory}/cities.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            city_id = row["city_id"]
            name = row["city_name"]
            country = row["country"]

  
            cities[city_id] = {
                "name": name,
                "country": country,
                "flights": set()
            }

            name_lower = name.lower()
            if name_lower not in city_name_to_ids:
                city_name_to_ids[name_lower] = set()
            city_name_to_ids[name_lower].add(city_id)

    with open(f"{directory}/airlines.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            airlines[row["airline_id"]] = row["airline_name"]

    with open(f"{directory}/flights.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            flight_id = row["flight_id"]
            source = row["source_city_id"]
            destination = row["destination_city_id"]

            if source in cities:
                cities[source]["flights"].add((flight_id, destination))


# -------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------

def neighbors_for_city(city_id):
    """
    Returns a set of (flight_id, city_id) pairs for all
    cities directly reachable from the given city_id.
    """
    if city_id in cities:
        return cities[city_id]["flights"]
    return set()


def get_city_id(city_name):
    """
    Returns the city_id for a given city name.
    If multiple IDs exist, returns the first one.
    Returns None if not found.
    """
    matches = city_name_to_ids.get(city_name.lower())
    if not matches:
        return None
    return next(iter(matches))


# -------------------------------------------------------
# SEARCH — BFS Shortest Path
# -------------------------------------------------------

class Node:
    """Represents a state in the search: which city we're at and how we got here."""
    def __init__(self, city_id, parent, action):
        self.city_id = city_id   # current city
        self.parent = parent     # the Node we came from
        self.action = action     # (flight_id, city_id) pair that got us here


class QueueFrontier:
    """BFS frontier using a queue (First In, First Out)."""
    def __init__(self):
        self.frontier = deque()

    def add(self, node):
        self.frontier.append(node)

    def is_empty(self):
        return len(self.frontier) == 0

    def remove(self):
        return self.frontier.popleft()

    def contains_city(self, city_id):
        return any(node.city_id == city_id for node in self.frontier)


def shortest_path(source, target):
    """
    Returns the shortest path from source city_id to target city_id
    as a list of (flight_id, city_id) tuples.
    Returns None if no path exists.
    """

    # Start at the source city with no parent and no action
    start = Node(city_id=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Keep track of cities we've already explored
    explored = set()

    while True:

        # If frontier is empty, no path exists
        if frontier.is_empty():
            return None

        # Take the next node from the frontier
        node = frontier.remove()

        # Mark this city as explored
        explored.add(node.city_id)

        # Look at all cities reachable from here
        for flight_id, city_id in neighbors_for_city(node.city_id):

            # Skip cities we've already visited
            if city_id in explored or frontier.contains_city(city_id):
                continue

            child = Node(city_id=city_id, parent=node, action=(flight_id, city_id))

            # Goal check — if this neighbor IS the target, return immediately
            if city_id == target:
                path = []
                while child.action is not None:
                    path.append(child.action)
                    child = child.parent
                path.reverse()
                return path

            # Otherwise add to frontier to explore later
            frontier.add(child)


def neighbors_for_city(city_id):
    """Returns a set of (flight_id, city_id) pairs for all cities reachable from city_id."""
    if city_id not in cities:
        return set()
    return cities[city_id]["flights"]
# -------------------------------------------------------
# MAIN — Entry point for testing data loading
# -------------------------------------------------------
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python flights.py [data_directory]")
        sys.exit(1)

    directory = sys.argv[1]

    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Get source city from user
    source_name = input("City: ").strip()
    source_id = get_city_id(source_name)
    if source_id is None:
        print(f"City '{source_name}' not found.")
        sys.exit(1)

    # Get target city from user
    target_name = input("City: ").strip()
    target_id = get_city_id(target_name)
    if target_id is None:
        print(f"City '{target_name}' not found.")
        sys.exit(1)

    # Find shortest path
    path = shortest_path(source_id, target_id)

    if path is None:
        print("No connection found between these cities.")
    else:
        print(f"{len(path)} flight connection(s).")
        current_id = source_id
        for i, (flight_id, city_id) in enumerate(path, start=1):
            current_name = cities[current_id]["name"]
            next_name = cities[city_id]["name"]
            print(f"{i}: {current_name} to {next_name}")
            current_id = city_id