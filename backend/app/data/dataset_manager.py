import pandas as pd


_active_dataset: pd.DataFrame | None = None


def set_active_dataset(df: pd.DataFrame) -> None:
    global _active_dataset

    _active_dataset = df


def get_active_dataset() -> pd.DataFrame:
    if _active_dataset is None:
        raise ValueError(
            "No dataset has been uploaded yet."
        )

    return _active_dataset


def clear_active_dataset() -> None:
    global _active_dataset

    _active_dataset = None