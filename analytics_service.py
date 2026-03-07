import psycopg2
import numpy as np
import json

DB_CONFIG = {
    "dbname": "rates",
    "user": "admin",
    "password": "admin",
    "host": "postgres_db",
    "port": "5432"
}

def fetch_rates():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT date, rate
        FROM exchange_rates
        WHERE base = 'EUR' AND target = 'HUF'
        ORDER BY date ASC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    dates = [row[0] for row in rows]
    rates = np.array([float(row[1]) for row in rows])

    return dates, rates


def calculate_analytics(rates):
    results = {}

    # Total return %
    total_return = (rates[-1] - rates[0]) / rates[0] * 100
    results["total_return_pct"] = round(total_return, 4)

    # Daily returns
    daily_returns = np.diff(rates) / rates[:-1]

    # Volatility
    volatility = np.std(daily_returns)
    results["daily_volatility"] = round(float(volatility), 6)

    # 30-day moving average
    if len(rates) >= 30:
        moving_avg_30 = np.mean(rates[-30:])
        results["moving_avg_30"] = round(float(moving_avg_30), 4)

    # 60-day moving average
        if len(rates) >= 60:
            moving_avg_60 = np.mean(rates[-60:])
            results["moving_avg_60"] = round(float(moving_avg_60), 4)

    # 90-day moving average
    if len(rates) >= 90:
        moving_avg_90 = np.mean(rates[-90:])
        results["moving_avg_90"] = round(float(moving_avg_90), 4)

    # Trend
    x = np.arange(len(rates))
    slope, intercept = np.polyfit(x, rates, 1)
    results["trend_slope"] = round(float(slope), 6)

    # Maximum drawdown
    cumulative_max = np.maximum.accumulate(rates)
    drawdown = (rates - cumulative_max) / cumulative_max
    max_drawdown = np.min(drawdown)
    results["max_drawdown"] = round(float(max_drawdown), 6)

    return results


def main():
    dates, rates = fetch_rates()

    if len(rates) < 2:
        print("Not enough data.")
        return

    analytics = calculate_analytics(rates)

    print(json.dumps(analytics, indent=4))

    with open("analytics.json", "w") as f:
        json.dump(analytics, f, indent=4)


if __name__ == "__main__":
    main()