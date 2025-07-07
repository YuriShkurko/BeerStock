import psycopg2
from beer_stock_db_driver import BeerStockDBDriver
from typing import List, Dict

class PostgresBeerStockDB(BeerStockDBDriver):
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()
        self.conn.autocommit = True
        # Drop table to make sure schema is correct (for dev/testing only)
        self.cur.execute("DROP TABLE IF EXISTS tap_list;")
        self.cur.execute("DROP TABLE IF EXISTS stock;")
        
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            base_price TEXT NOT NULL,
            min_price TEXT NOT NULL,
            max_price TEXT NOT NULL
        );
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS tap_list (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL REFERENCES stock(name) ON DELETE CASCADE,
            available BOOLEAN NOT NULL DEFAULT TRUE
        );
        """)

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
    def add_to_storage(self, name, base_price, min_price, max_price):
        self.cur.execute("SELECT name FROM stock WHERE name = %s;", (name,))
        if self.cur.fetchone():
            return False  # Already in stock


        self.cur.execute("""
            INSERT INTO stock (name, base_price, min_price, max_price)
            VALUES (%s, %s, %s, %s);
        """, (name, base_price, min_price, max_price))
        return True

    def release_beer(self, name):
        self.cur.execute("DELETE FROM stock WHERE name = %s;", (name,))
        return self.cur.rowcount > 0

    def list_beer(self, name):
        self.cur.execute("SELECT name FROM stock WHERE LOWER(name) = LOWER(%s);", (name,))
        row = self.cur.fetchone()
        if not row:
            return "not_found"

        # Check if it's already listed
        self.cur.execute("SELECT name FROM tap_list WHERE name = %s;", (name,))
        if self.cur.fetchone():
            return "already_listed"

        # Add to tap_list
        self.cur.execute("INSERT INTO tap_list (name, available) VALUES (%s, TRUE);", (name,))
        return "listed"
    

    def delist_beer(self, name):
        self.cur.execute("DELETE FROM tap_list WHERE name = %s;", (name,))
        return self.cur.rowcount > 0

    def hold_beer(self, name):
        self.cur.execute("UPDATE tap_list SET available = FALSE WHERE name = %s;", (name,))
        return self.cur.rowcount > 0

    def unhold_beer(self, name):
        self.cur.execute("UPDATE tap_list SET available = TRUE WHERE name = %s;", (name,))
        return self.cur.rowcount > 0

    def get_tap_list(self):
        self.cur.execute("SELECT name, price, available FROM tap_list;")
        results = self.cur.fetchall()
        return [{"name": name, "price": price, "available": available} for name, price, available in results]

    def customer_purchase_beer(self, name):
        self.cur.execute("SELECT available FROM tap_list WHERE name = %s;", (name,))
        row = self.cur.fetchone()
        return row and row[0] == True
