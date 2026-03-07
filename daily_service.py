import requests
import psycopg2
from datetime import datetime, timezone, timedelta
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

def get_last_saved_date(cur):
    cur.execute("""
        SELECT MAX(date)
        FROM exchange_rates
        WHERE base = %s AND target = %s
    """, (BASE, TARGET))

    result = cur.fetchone()[0]
    return result


def fetch_new_rates(start_date):
    today = datetime.now().strftime("%Y-%m-%d")

    url = f"https://api.frankfurter.dev/v1/{start_date}..{today}?symbols={TARGET}"

    print(f"Fetching data from {start_date} to {today}")
    response = requests.get(url, timeout=30)

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
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        last_date = get_last_saved_date(cur)

        if last_date is None:
            print("No existing data found. Run bootstrap_service first.")
            return

        next_date = last_date + timedelta(days=1)

        if next_date > datetime.now().date():
            print("Database already up to date.")
            return

        rates_dict = fetch_new_rates(next_date.strftime("%Y-%m-%d"))

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


if __name__ == "__main__":
    main()