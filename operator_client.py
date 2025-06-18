import requests

class OperatorClient:
    def __init__(self, server_url='http://localhost:8000'):
        self.server_url = server_url

    def ListBeer(self, name):
        payload = {"name": name}
        try:
            response = requests.post(f"{self.server_url}/list", json=payload, timeout=3)
            if response.status_code == 200:
                resp = response.json()
                print(resp.get("status") or resp.get("error"))
                return resp.get("status") == "beer listed"
            else:
                print(f"Request failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
    
    def DeListBeer(self, name):
        payload = {"name": name}
        try:
            response = requests.post(f"{self.server_url}/delist", json=payload)
            if response.status_code == 200:
                print("Beer delisted successfully.")
                return True
            else:
                print(f"Failed to delist beer: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False

    def Hold(self, name):
        payload = {"name": name}
        try:
            response = requests.post(f"{self.server_url}/hold", json=payload)
            if response.status_code == 200:
                print("Beer put on hold successfully.")
                return True
            else:
                print(f"Failed to put beer on hold: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
        
    def Unhold(self, name):
        payload = {"name": name}
        try:
            response = requests.post(f"{self.server_url}/unhold", json=payload)
            if response.status_code == 200:
                print("Beer unheld successfully.")
                return True
            else:
                print(f"Failed to unhold beer: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
        
    def Release(self, name):
        payload = {"name": name}
        try:
            response = requests.post(f"{self.server_url}/release", json=payload)
            if response.status_code == 200:
                print("Beer removed from stock successfully.")
                return True
            else:
                print(f"Failed to remove beer from stock: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False

    def Purchase(self, name, price):
        payload = {"name": name, "price": price}
        try:
            response = requests.post(f"{self.server_url}/purchase", json=payload)
            if response.status_code == 200:
                print("Beer added to stock successfully.")
                return True
            else:
                print(f"Failed to add beer to stock: {response.text}")
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
