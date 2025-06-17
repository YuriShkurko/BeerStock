import json
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer as HTTPServer
from jinja2 import Template

class BeerStock:
    def __init__(self):
        self.tap_list = [
           # {"name": "Pale Ale", "price": "$5", "available": True}
           
           
     # you need to make sure it doesnt take ages to load, and make sure logic works, also add tests :) gl 
        ]
        self.stock = [
            {'name': 'Pale Ale', 'price': '$5'},
            {'name': 'Lager', 'price': '$4'},
            {'name': 'Stout', 'price': '$6'},
            {'name': 'IPA', 'price': '$5'}
        ]

    def get_tap_list(self):
        return self.tap_list

    def get_stock(self):
        return self.stock

    def list_beer(self, beer_name):
        if any(beer["name"] == beer_name for beer in self.tap_list):
            return "already_listed"

        for beer in self.stock:
            if beer["name"] == beer_name:
                self.tap_list.append({**beer, "available": True})
                return "listed"

        return "not_in_stock"
    
    def delist_beer(self, beer_name):
        original_len = len(self.tap_list)
        self.tap_list = [beer for beer in self.tap_list if beer["name"] != beer_name]
        return len(self.tap_list) < original_len
    
    def hold_beer(self, beer_name):
        for beer in self.tap_list:
            if beer["name"] == beer_name:
                beer["available"] = False
                return True
        return False
    
    def unhold_beer(self, beer_name):
        for beer in self.tap_list:
            if beer["name"] == beer_name:
                beer["available"] = True
                return True
        return False
    
    def release_beer(self, beer_name):
        # Remove from stock entirely
        before = len(self.stock)
        self.stock = [beer for beer in self.stock if beer["name"] != beer_name]
        return len(self.stock) < before


class BeerStockServer:
    def __init__(self, host='localhost', port=8000):
        self.beer_stock = BeerStock()
        self.server_address = (host, port)
        self.html_template = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Beer Menu</title>
                <style>
                    table {
                        width: 50%;
                        border-collapse: collapse;
                        margin: 50px auto;
                        font-family: Arial, sans-serif;
                    }
                    th, td {
                        border: 2px solid black;
                        padding: 20px;
                        text-align: center;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <table>
                    <tr>
                        <th>Beers</th>
                        <th>Prices</th>
                    </tr>
                    {% for beer in beers %}
                        <tr>
                            <td>{{ beer.name }}</td>
                            <td>{{ beer.price }}</td>
                            <td>{{ 'Unavailable' if beer.get('available', True) == False else 'Available' }}</td>
                        </tr>
                    {% endfor %}
                </table>
            </body>
            </html>
        '''

    def run(self):
        server = HTTPServer(self.server_address, self.make_handler())
        print(f"Server running at http://{self.server_address[0]}:{self.server_address[1]}/")
        server.serve_forever()

    def make_handler(self):
        beer_stock = self.beer_stock
        html_template = self.html_template
    
        class BeerTableHandler(BaseHTTPRequestHandler):
            
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    template = Template(html_template)
                    html = template.render(beers=beer_stock.get_tap_list())
                    self.wfile.write(html.encode('utf-8'))

                elif self.path == '/api/listed':
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(beer_stock.get_tap_list()).encode('utf-8'))

                else:
                    self.send_error(404, 'Page Not Found')

            def do_POST(self):
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)

                if self.path == '/list':
                    try:
                        data = json.loads(post_data)
                        name = data.get("name")
                        if name:
                            result = beer_stock.list_beer(name)
                            self.send_response(200)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()

                            if result == "listed":
                                self.wfile.write(b'{"status": "beer listed"}')
                            elif result == "already_listed":
                                self.wfile.write(b'{"status": "beer already listed"}')
                            else:
                                self.wfile.write(b'{"error": "beer not in stock"}')
                        else:
                            self.send_response(400)
                            self.end_headers()
                            self.wfile.write(b'{"error": "Missing name field"}')
                    except json.JSONDecodeError:
                        self.send_response(400)
                        self.end_headers()
                        self.wfile.write(b'{"error": "Invalid JSON"}')
                elif self.path == '/delist':
                    try:
                        data = json.loads(post_data)
                        name = data.get("name")
                        if name and beer_stock.delist_beer(name):
                            self.send_response(200)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            self.wfile.write(b'{"status": "beer removed from tap"}')
                        else:
                            self.send_response(404)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            self.wfile.write(b'{"error": "beer not found on tap"}')
                    except json.JSONDecodeError:
                        self.send_response(400)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'{"error": "Invalid JSON"}')
                elif self.path == '/hold':
                    try:
                        data = json.loads(post_data)
                        name = data.get("name")
                        if name and beer_stock.hold_beer(name):
                            self.send_response(200)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            self.wfile.write(b'{"status": "beer put on hold"}')
                        else:
                            self.send_response(404)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            self.wfile.write(b'{"error": "beer not found on tap"}')
                    except json.JSONDecodeError:
                        self.send_response(400)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'{"error": "Invalid JSON"}')
                elif self.path == '/unhold':
                    try:
                        data = json.loads(post_data)
                        name = data.get("name")
                        if name and beer_stock.unhold_beer(name):
                            self.send_response(200)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            self.wfile.write(b'{"status": "beer unheld"}')
                        else:
                            self.send_response(404)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            self.wfile.write(b'{"error": "beer not found on tap"}')
                    except json.JSONDecodeError:
                        self.send_response(400)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'{"error": "Invalid JSON"}')
                elif self.path == '/release':
                    try:
                        data = json.loads(post_data)
                        name = data.get("name")
                        if name and beer_stock.release_beer(name):
                            self.send_response(200)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            self.wfile.write(b'{"status": "beer removed from stock"}')
                        else:
                            self.send_response(404)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            self.wfile.write(b'{"error": "beer not in stock"}')
                    except json.JSONDecodeError:
                        self.send_response(400)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'{"error": "Invalid JSON"}')
                else:
                    self.send_error(404, 'Page Not Found')
                    
        return BeerTableHandler        
            
            
    
if __name__ == '__main__':
    server = BeerStockServer()
    server.run()
