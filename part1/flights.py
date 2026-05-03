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
    print(f"  Cities loaded : {len(cities)}")
    print(f"  Airlines loaded: {len(airlines)}")

    # Quick test — show neighbors of Windhoek
    test_city = "Windhoek"
    city_id = get_city_id(test_city)
    if city_id:
        print(f"\nNeighbors of {test_city} (city_id={city_id}):")
        for flight_id, dest_id in neighbors_for_city(city_id):
            dest_name = cities[dest_id]["name"] if dest_id in cities else "Unknown"
            print(f"  Flight {flight_id} -> {dest_name}")
    else:
        print(f"\nCity '{test_city}' not found in dataset.")