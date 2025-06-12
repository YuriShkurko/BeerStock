from beer_server import GetBeerPrices, AddBeerPrice

def test_GetBeerPrices_matches_expected():
    expected = [
        {"name": "Pale Ale", "price": "$5"},
        {"name": "Lager", "price": "$4"},
        {"name": "Stout", "price": "$6"}
    ]

    actual = GetBeerPrices()

    assert actual == expected
    
def test_AddBeerPrice_validate():
    
    excpected_entry = {"name": "IPA", "price": "$4"}
    succesful = AddBeerPrice(excpected_entry)
    assert succesful
    
    table = GetBeerPrices()
    assert excpected_entry in table