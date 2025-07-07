from beer_stock_db_driver import BeerStockDBDriver

class InMemoryBeerStockDB(BeerStockDBDriver):
    def __init__(self):
        # Internal dictionary to simulate storage
        self.storage = {}

    def add_to_storage(self, name, base_price, min_price, max_price):
        if name in self.storage:
            return False  # Already exists
        self.storage[name] = {
            "base_price": base_price,
            "min_price": min_price,
            "max_price": max_price
        }
        return True

    def get_from_storage(self, name):
        return self.storage.get(name)

    def remove_from_storage(self, name):
        return self.storage.pop(name, None) is not None

    def get_all_beers(self):
        return list(self.storage.items())
