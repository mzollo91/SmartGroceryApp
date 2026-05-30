class store_distance:
    def __init__(self, store_a_id: int, store_a_name: str, store_b_id: int, store_b_name: str, travel_distance_minutes: float, distance_id: int=None):
        self.distance_id = distance_id # Database primary key
        self.store_a_id = store_a_id
        self.store_a_name = store_a_name
        self.store_b_id = store_b_id
        self.store_b_name = store_b_name
        self.travel_distance_minutes = travel_distance_minutes

    def __repr__(self):
        return f"store_distance(id={self.distance_id}, a={self.store_a_id}, b={self.store_b_id}, time={self.travel_distance_minutes})"

    def __str__(self):
        return f"{self.store_a_name} -> {self.store_b_name}: {self.travel_distance_minutes} minutes."

    def save_to_db(self, db_manager):
        db_manager.add_distance(self)