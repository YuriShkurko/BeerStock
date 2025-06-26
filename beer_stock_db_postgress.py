import psycopg2
from beer_stock_db_driver import BeerStockDBDriver

class PostgresBeerStockDB(BeerStockDBDriver):
    def __init__(self, conn):
        self.conn = conn

    def add_to_storage(self, name, base_price, min_price, max_price):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO stock (name, base_price, min_price, max_price) VALUES (%s, %s, %s, %s);",
                (name, base_price, min_price, max_price)
            )

    def get_from_storage(self, name):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT name, base_price, min_price, max_price FROM stock WHERE name = %s;",
                (name,)
            )
            row = cur.fetchone()
            return {
                "name": row[0],
                "base_price": row[1],
                "min_price": row[2],
                "max_price": row[3]
            } if row else None

    def remove_from_storage(self, name):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM stock WHERE name = %s;", (name,))
            return cur.rowcount > 0

    def get_all_beers(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT name, base_price, min_price, max_price FROM stock;")
            return [
                {
                    "name": row[0],
                    "base_price": row[1],
                    "min_price": row[2],
                    "max_price": row[3]
                }
                for row in cur.fetchall()
            ]
