import requests
import psycopg2
from psycopg2 import sql
from datetime import datetime, timezone
import sys


DB_CONFIG = {
    "dbname": "rates",
    "user": "admin",
    "password": "admin",
    "host": "postgres_db",
    "port": "5432"
}

BASE = "EUR"
TARGET = "HUF"
START_DATE = "2024-01-01"
API_URL = f"https://api.frankfurter.dev/v1/{START_DATE}..?symbols={TARGET}"


def create_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            id SERIAL PRIMARY KEY,
            base VARCHAR(10) NOT NULL,
            target VARCHAR(10) NOT NULL,
            rate NUMERIC NOT NULL,
            date DATE NOT NULL,
            created_at TIMESTAMPTZ NOT NULL,
            UNIQUE(base, target, date)
        )
    """)


def fetch_rates():
    print("Fetching historical data...")
    response = requests.get(API_URL, timeout=30)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")

    data = response.json()
    return data["rates"]


def save_rates(cur, rates_dict):
    inserted = 0

    for date_str, value in rates_dict.items():
        rate = value[TARGET]

        cur.execute("""
            INSERT INTO exchange_rates (base, target, rate, date, created_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (base, target, date) DO NOTHING
        """, (
            BASE,
            TARGET,
            rate,
            date_str,
            datetime.now(timezone.utc)
        ))

        if cur.rowcount > 0:
            inserted += 1

    return inserted


def main():
	conn = None
	cur = None

	try:
		print("Connecting to database...")
		conn = psycopg2.connect(**DB_CONFIG)
		cur = conn.cursor()

		create_table(cur)
		conn.commit()

		rates_dict = fetch_rates()

		print(f"Received {len(rates_dict)} days of data.")

		inserted = save_rates(cur, rates_dict)
		conn.commit()

		print(f"Inserted {inserted} new rows.")

	except Exception as e:
		print("ERROR:", e)
		if conn:
			conn.rollback()
		sys.exit(1)

	finally:
        	if cur:
           		cur.close()
        	if conn:
            		conn.close()

        	print("Connection closed.")


if __name__ == "__main__":
    main()