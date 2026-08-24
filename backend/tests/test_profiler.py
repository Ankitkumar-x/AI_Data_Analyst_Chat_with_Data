import pandas as pd

from app.data.profiler import profile_dataset


def test_profile_dataset():

    df = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr"],
        "Product": [
            "Laptop",
            "Phone",
            "Table",
            "Chair",
        ],
        "Sales": [
            50000,
            30000,
            15000,
            10000,
        ],
        "Profit": [
            8000,
            5000,
            3000,
            2000,
        ],
    })

    result = profile_dataset(df)

    assert result["rows"] == 4
    assert result["columns"] == 4

    assert "Sales" in result["numerical_columns"]
    assert "Profit" in result["numerical_columns"]

    assert "Product" in result["categorical_columns"]

    assert "Month" in result["month_columns"]

    assert result["date_columns"] == []

    assert result["missing_values"]["Sales"] == 0

    assert result["duplicate_rows"] == 0

    assert "Sales" in result["numerical_statistics"]

    assert "Sales" in result["kpis"]

    assert "correlation_matrix" in result

    assert "data_quality" in result