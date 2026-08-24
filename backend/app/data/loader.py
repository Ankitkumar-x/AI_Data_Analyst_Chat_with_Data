import pandas as pd
from pathlib import Path


def load_dataset(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)

    elif path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file format")