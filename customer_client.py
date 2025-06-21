import requests

class CustomerClient:
    
    def __init__(self, server_url='http://localhost:8000'):
        self.server_url = server_url
        
    def PurchaseBeer(self, name):
        payload = {"name": name}
        try:
            response = requests.post(f"{self.server_url}/customer/purchase", json=payload, timeout=3)
            if response.status_code == 200:
                resp = response.json()
                print(resp.get("status") or resp.get("error"))
                return f"Order placed for {name}"
            else:
                print(f"{response.status_code}")
                return "Beer not available"
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
        
        
