import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()


def get_engine():
    url = os.getenv("DATABASE_URL")
    if not url: raise RuntimeError("DATABASE_URL is not configured. Copy .env.example to .env and set credentials.")
    return create_engine(url, pool_pre_ping=True, future=True)


def load_to_postgres(df: pd.DataFrame, table_name: str = "superstore_orders") -> int:
    engine = get_engine()
    with engine.begin() as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False, method="multi", chunksize=1000)
        conn.execute(text(f'CREATE INDEX IF NOT EXISTS idx_{table_name}_order_date ON {table_name} (order_date)'))
        conn.execute(text(f'CREATE INDEX IF NOT EXISTS idx_{table_name}_region ON {table_name} (region)'))
    return len(df)


def read_from_postgres(table_name: str = "superstore_orders") -> pd.DataFrame:
    with get_engine().connect() as conn:
        return pd.read_sql(text(f'SELECT * FROM {table_name}'), conn)
