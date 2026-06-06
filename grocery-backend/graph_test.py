from graph import GroceryStoreGraph

graph = GroceryStoreGraph()

locations = ["Bakery",
             "Produce",
             "Dairy",
             "Deli",
             "Entrance",
             "Check-out"]

for location in locations:
    if graph.add_location(location_name=location):
        print(f"'{location}'' successfully added")
    else:
        print(f"'{location}'' already exists")

path_list = {"Bakery": (["Produce", 10],),
         "Produce": (["Dairy", 5], ["Deli", 15]),
         "Dairy": (["Entrance", 20], ["Deli", 5]),
         "Entrance": (["Check-out", 5],)}

for location, paths in path_list.items():
    for zone in paths:
        graph.add_path(from_loc=location, to_loc=zone[0],distance=zone[1])

print(f"{graph.get_all_locations()}\n")

graph.display_store_map()