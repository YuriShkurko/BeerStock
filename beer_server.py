import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Template

global_beer_prices = [
        {'name': 'Pale Ale', 'price': '$5'},
        {'name': 'Lager', 'price': '$4'},
        {'name': 'Stout', 'price': '$6'},
    ]

def GetBeerPrices():
    return global_beer_prices

def AddBeerPrice(entry):
    global_beer_prices.append(entry)
    return True
    
def main():
    
    beers = GetBeerPrices()
    
    html_template = '''
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
    
    

    class BeerTableHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                template = Template(html_template)
                html = template.render(beers=beers)
                self.wfile.write(html.encode('utf-8'))
            else:
                self.send_error(404, 'Page Not Found')
        
        def do_POST(self):
            if self.path == '/add':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data)
                    print(data)
                    if "name" in data and "price" in data:
                        AddBeerPrice({"name": data["name"], "price": data["price"]})
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

            

    server_address = ('', 8000)
    httpd = HTTPServer(server_address, BeerTableHandler)
    print("Server running at http://localhost:8000/")
    httpd.serve_forever()

if __name__ == '__main__':
    main()
