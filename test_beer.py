from beer_server import GetBeerPrices, AddBeerPrice, GetStock
from beer_server import Operator

def test_GetBeerPrices_matches_expected():
    expected = [
        
    ]

    actual = GetBeerPrices()

    assert actual == expected
    
def test_AddBeerPrice_validate():
    
    excpected_entry = {"name": "IPA", "price": "$4"}
    succesful = AddBeerPrice(excpected_entry)
    assert succesful
    
    table = GetBeerPrices()
    assert excpected_entry in table
    
def test_ListBeer_validate():
    
    expected_entry = "IPA"
    stock = GetStock()
    listing = GetBeerPrices()
    operator = Operator(stock, listing)
    succesful = operator.ListBeer(expected_entry)
    assert succesful
    assert {"name": "IPA", "price": "$4"} in listing

    
    
    