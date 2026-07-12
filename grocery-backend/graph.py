class GroceryStoreGraph:
	def __init__(self):
		"""
		Initializes an empty store map.
		This is a dictionary matching string names
		to lists of tuples, i.e.
		{ "Location_A": [("Location_B", distance_in_feet), ("Location_C", distance)] }
	    """	
		self.adjacency_list = {}
		
	def add_location(self, location_name: str) -> bool:
		"""
		Adds a unique aisle, section, or entrance to the graph.
		Returns True if successful, or false if the location already exists.
		"""
		if location_name in self.adjacency_list:
			return False
		self.adjacency_list[location_name] = []
		return True

		
	def add_path(self, from_loc: str, to_loc: str, distance: int, bidirectional: bool = True) -> None:
		"""
		Creates a walkable path between two existing locations with a weight (distance).
		If bidirectional is True, then the path links both ways (A -> B and B -> A).
		"""
		if from_loc not in self.adjacency_list or to_loc not in self.adjacency_list:
			missing = []
			if from_loc not in self.adjacency_list: missing.append(from_loc)
			if to_loc not in self.adjacency_list: missing.append(to_loc)
			raise KeyError(f"Location(s) missing from store map: {', '.join(missing)}") # Syntax of {', '.join(missing)} is to use ', ' as a delimiter between values in "missing" list.
		
		self.adjacency_list[from_loc].append((to_loc, distance))
		
		if bidirectional:
			self.adjacency_list[to_loc].append((from_loc, distance))

		return
		
	def get_neighbors(self, location_name: str) -> list:
		"""
		Returns a list of tuples representing all locations directly accessible
		from a given location, along with their distances.
		Example: [("Bakery", 12), ("Dairy", 45)]
		"""
		if location_name not in self.adjacency_list:
			raise KeyError(f"{location_name} not found in store map.")
		
		return self.adjacency_list[location_name]
		
	def get_all_locations(self) -> list:
		"""
		Returns a simple list of all locations registered in the store map.
		This will be helpful for the UI.
		"""
		return list(self.adjacency_list.keys())
		
	def display_store_map(self) -> None:
		"""
		A clean terminal printout helper to visually verify the storw floor plan.
		Helpful for debugging purposes.
		"""
		for location, paths in self.adjacency_list.items():
			print(f"Location '{location}' is adjacent to:")
			if paths is not None:
				for zone, distance in paths:
					print(f"-> {zone} ({distance} ft)")

	def map_initialize(self) -> None:
		"""
		An initial seed of the map.
		"""
		locations = ["Bakery",
				 "Produce",
				 "Dairy",
				 "Deli",
				 "Entrance",
				 "Check-out"]

		for location in locations:
			if self.add_location(location_name=location):
				print(f"'{location}' successfully added")
			else:
				print(f"'{location}' already exists")

		path_list = {"Bakery": (["Produce", 10],),
				 "Produce": (["Dairy", 5], ["Deli", 15]),
				 "Dairy": (["Entrance", 20], ["Deli", 5]),
				 "Entrance": (["Check-out", 5],)}

		for location, paths in path_list.items():
			for zone in paths:
				self.add_path(from_loc=location, to_loc=zone[0],distance=zone[1])