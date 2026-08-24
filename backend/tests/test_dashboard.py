import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from app.data.dataset_manager import set_active_dataset


client = TestClient(app)


def test_dashboard_summary():

    df = pd.DataFrame({
        "Product": ["Laptop", "Phone", "Table", "Chair"],
        "Category": [
            "Technology",
            "Technology",
            "Furniture",
            "Furniture",
        ],
        "Sales": [50000, 30000, 15000, 10000],
        "Profit": [8000, 5000, 3000, 2000],
        "Region": ["West", "East", "West", "Central"],
    })

    set_active_dataset(df)

    response = client.get("/api/dashboard")

    assert response.status_code == 200

    data = response.json()

    assert data["rows"] == 4
    assert data["columns"] == 5

    assert "numerical_columns" in data
    assert "categorical_columns" in data
    assert "numerical_statistics" in data
    assert "kpis" in data
    assert "data_quality" in data
    assert "correlation_matrix" in data


def test_dashboard_visualizations():

    df = pd.DataFrame({
        "Product": ["Laptop", "Phone", "Table", "Chair"],
        "Category": [
            "Technology",
            "Technology",
            "Furniture",
            "Furniture",
        ],
        "Sales": [50000, 30000, 15000, 10000],
        "Profit": [8000, 5000, 3000, 2000],
        "Region": ["West", "East", "West", "Central"],
    })

    set_active_dataset(df)

    response = client.get(
        "/api/dashboard/visualizations"
    )

    assert response.status_code == 200

    data = response.json()

    assert "charts" in data
    assert len(data["charts"]) > 0

    chart_types = {
        chart["chart_type"]
        for chart in data["charts"]
    }

    assert "bar" in chart_types
    assert "scatter" in chart_types