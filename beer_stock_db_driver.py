from abc import ABC, abstractmethod

class BeerStockDBDriver(ABC):
    @abstractmethod
    def add_to_storage(self, name, base_price, min_price, max_price):
        pass

    @abstractmethod
    def get_from_storage(self, name):
        pass

    @abstractmethod
    def remove_from_storage(self, name):
        pass

    @abstractmethod
    def get_all_beers(self):
        pass
