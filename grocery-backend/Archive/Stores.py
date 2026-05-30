class store_cl:
    def __init__(self, name: str, street_address: str, city: str, state: str, zip_code: str,store_id: int = None):
        self.name = name
        self.store_id = store_id # Database primary key
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __repr__(self):
        return f"<Store: {self.name}, {self.street_address}, {self.city}, {self.state}, ({self.zip_code})>"

    def save_to_db(self, db_manager):
        db_manager.insert_store(self)