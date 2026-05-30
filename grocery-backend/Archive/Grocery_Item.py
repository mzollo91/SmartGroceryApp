class grocery_item:
    def __init__(self, name: str, weight_or_count: float,units: str, department_location: str = None, item_id: int = None):
        self.name = name
        self.department_location = department_location
        self.weight_or_count = weight_or_count
        self.units = units
        self.item_id = item_id # Database primary key

    def __repr__(self):
        return f"<Item: {self.name}, {self.weight_or_count} {self.units}, in {self.department_location}>"
    
    def save_to_db(self, db_manager):
        db_manager.insert_item(self)
