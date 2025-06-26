import psycopg2
import pytest
import socket
from beer_server import BeerStock  # this is your new DB-backed class
from beer_stock_db_postgress import PostgresBeerStockDB

@pytest.fixture(scope="module")
def db_conn():
    import docker
    import time

    client = docker.from_env()
    try:
        old = client.containers.get("test_pg")
        old.stop()
        old.remove()
    except docker.errors.NotFound:
        pass

    container = client.containers.run(
        "postgres:15",
        name="test_pg",
        ports={'5432/tcp': 5432},
        environment={
            'POSTGRES_DB': 'beer_test',
            'POSTGRES_USER': 'postgres',
            'POSTGRES_PASSWORD': 'postgres',
        },
        detach=True
    )

    time.sleep(5)  # wait for db to start

    conn = psycopg2.connect(
        dbname="beer_test",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS stock;")
    cur.execute("""
                CREATE TABLE stock (
                id SERIAL PRIMARY KEY,
                name TEXT,
                base_price TEXT,
                min_price TEXT,
                max_price TEXT
        );

    """)

    yield conn

    cur.close()
    conn.close()
    container.stop()
    container.remove()

def test_add_beer_db(db_conn):
    stock = BeerStock(PostgresBeerStockDB(db_conn))  # pass the connection to your BeerStock class
    stock.add_to_storage("IPA", "$5", "$4", "$6")  # List the beer first
    ipa = stock.get_from_storage("IPA")     
    assert ipa["name"] == "IPA"
    assert ipa["base_price"] == "$5"
    assert ipa["min_price"] == "$4"
    assert ipa["max_price"] == "$6"

