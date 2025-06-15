import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Template

class BeerStock:
    def __init__(self):
        self.tap_list = []
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

    def list_beer(self, entry):
        self.tap_list.append(entry)
        return True
    
    def list_beer_from_stock(self, beer_name):
        for beer in self.stock:
            if beer["name"] == beer_name:
                self.tap_list.append(beer)
                return True
        return False


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

                if self.path == '/add':
                    try:
                        data = json.loads(post_data)
                        if "name" in data and "price" in data:
                            beer_stock.list_beer({"name": data["name"], "price": data["price"]})
                            self.send_response(200)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            self.wfile.write(b'{"status": "success"}')
                        else:
                            self.send_response(400)
                            self.end_headers()
                            self.wfile.write(b'{"error": "Missing fields"}')
                    except json.JSONDecodeError:
                        self.send_response(400)
                        self.end_headers()
                        self.wfile.write(b'{"error": "Invalid JSON"}')

                else:
                    self.send_error(404, 'Page Not Found')

        return BeerTableHandler
    
if __name__ == '__main__':
    server = BeerStockServer()
    server.run()
