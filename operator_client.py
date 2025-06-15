import requests

class OperatorClient:
    def __init__(self, server_url='http://localhost:8000'):
        self.server_url = server_url

    def ListBeer(self, name, price):
        payload = {"name": name, "price": price}
        try:
            response = requests.post(f"{self.server_url}/add", json=payload)
            if response.status_code == 200:
                print("Beer listed successfully.")
                return True
            else:
                print(f"Failed to list beer: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False

    def ShowListedBeer(self):
        try:
            response = requests.get(f"{self.server_url}/api/listed")
            if response.status_code == 200:
                beers = response.json()
                return beers
            else:
                print(f"Failed to fetch listed beers: {response.text}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []
