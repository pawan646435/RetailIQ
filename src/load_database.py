from src.data_loader import PROCESSED_DIR
from src.database import load_to_postgres
import pandas as pd

if __name__ == "__main__":
    path = PROCESSED_DIR / "superstore_cleaned.csv"
    if not path.exists(): raise SystemExit("Run `python -m src.prepare_data` first.")
    df = pd.read_csv(path, parse_dates=["order_date", "ship_date", "month_year"])
    count = load_to_postgres(df)
    print(f"Loaded {count:,} records into public.superstore_orders")
