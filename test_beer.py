from beer_server import BeerStock

def test_list_and_delist_beer():
    stock = BeerStock()
    
    assert stock.list_beer("IPA") == "listed"
    assert {"name": "IPA", "price": "$5", "available": True} in stock.get_tap_list()

    assert stock.delist_beer("IPA")
    assert all(b["name"] != "IPA" for b in stock.get_tap_list())

def test_hold_and_unhold_beer():
    stock = BeerStock()

    stock.list_beer("IPA")
    assert stock.hold_beer("IPA")
    assert any(b["name"] == "IPA" and b["available"] is False for b in stock.get_tap_list())

    assert stock.unhold_beer("IPA")
    assert any(b["name"] == "IPA" and b["available"] is True for b in stock.get_tap_list())

def test_release_beer_removes_from_stock():
    stock = BeerStock()

    assert stock.release_beer("IPA")
    assert all(beer["name"] != "IPA" for beer in stock.get_stock())