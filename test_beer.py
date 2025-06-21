from beer_server import BeerStock
from customer_client import CustomerClient
from operator_client import OperatorClient


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

def test_order_beer_valid():
    operator = OperatorClient("http://localhost:8000")
    customer = CustomerClient("http://localhost:8000")

    # Ensure beer is on the tap list and available
    operator.ListBeer("IPA")
    operator.Unhold("IPA")

    assert customer.PurchaseBeer("IPA") == "Order placed for IPA"
    assert customer.PurchaseBeer("Nonexistent Beer") == "Beer not available"

def test_purchase_beer_adds_new_beer():
    stock = BeerStock()
    new_name = "Test Beer"
    new_price = "$7"
    assert stock.purchase_beer(new_name, new_price) is True
    assert any(beer["name"] == new_name and beer["price"] == new_price for beer in stock.get_stock())

def test_purchase_beer_duplicate():
    stock = BeerStock()
    existing_name = stock.get_stock()[0]["name"]
    existing_price = stock.get_stock()[0]["price"]
    assert stock.purchase_beer(existing_name, existing_price) is False
    # Ensure only one instance in stock
    assert [beer["name"] for beer in stock.get_stock()].count(existing_name) == 1
