# EUR → HUF Exchange Rate Dashboard

This project provides a complete pipeline for downloading, processing, analyzing, and visualizing EUR/HUF exchange rates.

---

## Requirements

You need to have Docker installed on your local machine (download from [docker.com](https://www.docker.com/)).  
No additional applications are required – Docker will handle all dependencies and service setup.

---

## Project Services

This project contains the following services:

### 1. Bootstrap Service
- Downloads EUR/HUF exchange rates starting from 01/01/2024.  
- Saves this information to a PostgreSQL database called `rates`.  
- Database table: `exchange_rates` with the following schema:

| Column     | Type      | Description                                         |
|------------|----------|-----------------------------------------------------|
| id         | PK       | Primary key                                         |
| base       | VARCHAR  | Base currency                                       |
| target     | VARCHAR  | Target currency                                     |
| rate       | NUMERIC  | Exchange rate of base/target                        |
| date       | DATE     | Daily closing date of exchange rate                 |
| created_at | TIMESTAMPTZ | Timestamp when the record was saved              |

**Notes:** Records are unique based on the combination of base currency, target currency, and date.

---

### 2. Daily Service
- Checks the latest date in the `exchange_rates` table.  
- Updates the table with the most recent exchange rates if missing.

---

### 3. Analytics Service
- Uses the data in `exchange_rates` to calculate financial indicators and saves them to a JSON file:

  - Total return (from 01/01/2024 to the last saved date)  
  - Daily volatility  
  - Moving averages: 30, 60, 90 days  
  - Trend  
  - Maximum drawdown

---

### 4. Dashboard
- Uses Streamlit to visualize the analytics.  
- Available at [http://localhost:8501](http://localhost:8501).

---
    
## Running Services

### 1. Start the PostgreSQL database
```bash
docker-compose up -d postgres_db
```

### 2. Run the workers and services

```
docker-compose run --rm bootstrap_worker
docker-compose run --rm daily_worker
docker-compose run --rm analytics_worker
docker-compose up dashboard
```

Notes: Make sure port 8501 is free on your host machine before starting the dashboard.
No local Python or dependencies are required; Docker handles everything.

---

### Docker Hub Images

All project services are also available as pre-built images on Docker Hub.
You can pull and run them directly without building locally.

| Service           | Docker Hub Image                     |
|-------------------|--------------------------------------|
| PostgreSQL        | vamosz92/app-postgres_db:latest      |
| Bootstrap Worker  |vamosz92/app-bootstrap_worker:latest  |
| Daily Worker      | vamosz92/app-daily_worker:v1         |
| Analytics Worker  | vamosz92/app-analytics_worker:v1     |
| Dashboard         | vamosz92/app-dashboard:latest        |

Example: Pull and Run

```
docker pull vamosz92/app-dashboard:latest
docker run -p 8501:8501 vamosz92/app-dashboard:latest
```

This allows you to run the service without building it locally.
Other services can be pulled similarly using their Docker Hub images.

Notes

- The dashboard displays key metrics (total return, volatility, moving averages, trend, max drawdown).
- Docker ensures all dependencies are handled, so no local Python setup is required.
