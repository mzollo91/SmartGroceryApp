import datetime
class price_record:
    def __init__(self, item_id: int, store_id: int, price: float, date_recorded: datetime, price_id: int = None):
        self.item_id = item_id
        self.store_id = store_id
        self.price = price
        if date_recorded is None:
            self.date_recorded = datetime.date.today()
        else:
            self.date_recorded = date_recorded # Last recorded date of price
        self.price_id = price_id

    def __repr__(self):
        return f"<Item ID: {self.item_id}, Store ID: {self.store_id}, Price: ${self.price}, Recorded On: {self.date_recorded}>"