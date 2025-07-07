import pytest
from in_memory_beer_stock_db import InMemoryBeerStockDB
from beer_server import BeerStock, BeerStockServer
import time
import threading
from operator_client import OperatorClient

@pytest.fixture
def memory_db():
    return InMemoryBeerStockDB()

@pytest.fixture(scope="module")
def db_in_mem_seeded():
    # Just returning the in-memory DB instance here
    db = InMemoryBeerStockDB()
    # Pre-populate it like the previous test did
    db.add_to_storage("IPA", "$5", "$4.50", "$5.50")
    db.add_to_storage("Lager", "$4", "$3.60", "$4.40")
    return db

@pytest.fixture(scope="module")
def beer_server_in_mem_db(db_in_mem_seeded):
    stock = BeerStock(db_driver=db_in_mem_seeded)
    server = BeerStockServer(beer_stock=stock)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    time.sleep(1)  # Wait for server to start
    yield server
    
@pytest.fixture
def operator_localhost8000(beer_server):
    return OperatorClient(server_url="http://localhost:8000")