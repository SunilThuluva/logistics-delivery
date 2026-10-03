
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = (
    PROJECT_ROOT / "data" / "raw" / "logistics_data.csv"
)

CLEAN_DATA_PATH = (
    PROJECT_ROOT / "data" / "cleaned" / "logistics_cleaned.csv"
)


def load_data(path=RAW_DATA_PATH):
    """Load the original CSV dataset."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    return pd.read_csv(path)


def save_data(df, path=CLEAN_DATA_PATH):
    """Save cleaned data to a CSV file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(path, index=False)

    return path