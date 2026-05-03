import sys
sys.path.insert(0, ".")

from flights import load_data, shortest_path, get_city_id, cities

print("=" * 50)
print("RUNNING PART 1 TEST CASES")
print("=" * 50)

load_data("data")

test_cases = [
    ("Windhoek", "Cairo"),
    ("Windhoek", "Johannesburg"),
    ("Johannesburg", "Nairobi"),
]

for source_name, target_name in test_cases:
    source_id = get_city_id(source_name)
    target_id = get_city_id(target_name)

    if source_id is None or target_id is None:
        print(f"\n[SKIP] One of the cities not found: {source_name}, {target_name}")
        continue

    path = shortest_path(source_id, target_id)

    print(f"\nRoute: {source_name} -> {target_name}")
    if path is None:
        print("  No connection found.")
    else:
        print(f"  {len(path)} flight connection(s).")
        current_id = source_id
        for i, (flight_id, city_id) in enumerate(path, start=1):
            current_name = cities[current_id]["name"]
            next_name = cities[city_id]["name"]
            print(f"  {i}: {current_name} to {next_name}")
            current_id = city_id

print("\n" + "=" * 50)
print("ALL TESTS COMPLETE")
print("=" * 50)