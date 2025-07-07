import pytest
from operator_client import OperatorClient 

@pytest.fixture
def operator(beer_server_in_mem_db):
    return OperatorClient(server_url="http://localhost:8000")

def test_list_and_delist_beer(operator, db_in_mem_seeded, beer_server_in_mem_db):

    print(db_in_mem_seeded.get_all_beers())
    print(beer_server_in_mem_db.beer_stock.get_storage())
    assert operator.ListBeer("IPA") is True
    assert db_in_mem_seeded.tap_list["IPA"]["available"] is True
    assert operator.DeListBeer("IPA") is True
    assert "IPA" not in db_in_mem_seeded.tap_list
    


def test_hold_and_unhold_beer(operator, db_conn):
    cur = db_conn.cursor()
    assert operator.ListBeer("Lager") is True
    assert operator.Hold("Lager") is True
    cur.execute("SELECT available FROM tap_list WHERE name = %s;", ("Lager",))
    assert cur.fetchone()[0] is False
    assert operator.Unhold("Lager") is True
    cur.execute("SELECT available FROM tap_list WHERE name = %s;", ("Lager",))
    assert cur.fetchone()[0] is True
    cur.close()

def test_purchase_and_release(operator, db_in_mem_seeded):
    
    assert operator.Purchase("Pale Ale", "$6") is True
    pale_ale = db_in_mem_seeded.get_from_storage("Pale Ale")
    assert pale_ale is not None
    assert operator.Release("Pale Ale") is True
    assert db_in_mem_seeded.get_from_storage("Pale Ale") is None
