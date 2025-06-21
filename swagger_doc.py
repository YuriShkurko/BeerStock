# swagger_doc.py

SWAGGER_JSON = {
    "openapi": "3.0.0",
    "info": {
        "title": "BeerStock API",
        "version": "1.0.0",
        "description": "API for managing beer stock, tap list, and customer orders."
    },
    "paths": {
        "/api/listed": {
            "get": {
                "summary": "Get tap list",
                "responses": {
                    "200": {
                        "description": "List of beers on tap",
                        "content": {
                            "application/json": {
                                "schema": {"type": "array", "items": {"type": "object"}}
                            }
                        }
                    }
                }
            }
        },
        "/list": {
            "post": {
                "summary": "List a beer on tap",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object", "properties": {"name": {"type": "string"}}}
                        }
                    }
                },
                "responses": {"200": {"description": "Beer listed"}, "400": {"description": "Error"}}
            }
        },
        "/delist": {
            "post": {
                "summary": "Remove a beer from tap",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object", "properties": {"name": {"type": "string"}}}
                        }
                    }
                },
                "responses": {"200": {"description": "Beer removed"}, "404": {"description": "Not found"}}
            }
        },
        "/hold": {
            "post": {
                "summary": "Put a beer on hold",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object", "properties": {"name": {"type": "string"}}}
                        }
                    }
                },
                "responses": {"200": {"description": "Beer on hold"}, "404": {"description": "Not found"}}
            }
        },
        "/unhold": {
            "post": {
                "summary": "Unhold a beer",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object", "properties": {"name": {"type": "string"}}}
                        }
                    }
                },
                "responses": {"200": {"description": "Beer unheld"}, "404": {"description": "Not found"}}
            }
        },
        "/purchase": {
            "post": {
                "summary": "Add a beer to stock",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object", "properties": {"name": {"type": "string"}, "price": {"type": "string"}}}
                        }
                    }
                },
                "responses": {"200": {"description": "Beer added"}, "400": {"description": "Already in stock or missing fields"}}
            }
        },
        "/release": {
            "post": {
                "summary": "Remove a beer from stock",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object", "properties": {"name": {"type": "string"}}}
                        }
                    }
                },
                "responses": {"200": {"description": "Beer removed"}, "404": {"description": "Not in stock"}}
            }
        },
        "/customer/purchase": {
            "post": {
                "summary": "Customer orders a beer",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"type": "object", "properties": {"name": {"type": "string"}}}
                        }
                    }
                },
                "responses": {"200": {"description": "Order placed"}, "404": {"description": "Beer not available"}}
            }
        }
    }
}

SWAGGER_UI_HTML = '''
<!DOCTYPE html>
<html>
<head>
  <title>BeerStock API Swagger UI</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      window.ui = SwaggerUIBundle({
        url: '/swagger.json',
        dom_id: '#swagger-ui',
      });
    };
  </script>
</body>
</html>
'''
