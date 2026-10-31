from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"


def locate_dataset() -> Path:
    candidates = [*RAW_DIR.glob("*.csv"), *RAW_DIR.glob("*.xlsx"), *RAW_DIR.glob("*.xls")]
    if not candidates:
        raise FileNotFoundError(
            "No dataset found. Place the Sample Superstore CSV/XLSX in data/raw/. "
            "See README.md for the official Tableau download source."
        )
    return candidates[0]


def load_raw_data(path: str | Path | None = None) -> pd.DataFrame:
    file_path = Path(path) if path else locate_dataset()
    if file_path.suffix.lower() == ".csv":
        try:
            return pd.read_csv(file_path, encoding="utf-8-sig")
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding="latin-1")
    if file_path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(
            file_path,
            sheet_name="Orders",
            engine="calamine"
        )
    raise ValueError(f"Unsupported dataset format: {file_path.suffix}")
