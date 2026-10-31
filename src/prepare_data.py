from src.data_loader import load_raw_data, PROCESSED_DIR
from src.data_cleaning import clean_data

if __name__ == "__main__":
    raw = load_raw_data()
    cleaned, report = clean_data(raw)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    target = PROCESSED_DIR / "superstore_cleaned.csv"
    cleaned.to_csv(target, index=False)
    print(f"Saved {len(cleaned):,} rows to {target}")
    print("Cleaning report:")
    for key, value in report.items(): print(f"  {key}: {value}")
