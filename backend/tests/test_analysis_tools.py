import pandas as pd
import pytest

def test_calculate_sum(sample_df):
    result = calculate_sum(
        sample_df,
        "Sales"
    )

    assert result == 105000.0


def test_calculate_average(sample_df):
    result = calculate_average(
        sample_df,
        "Sales"
    )

    assert result == 26250.0


def test_top_n_analysis(sample_df):
    result = top_n_analysis(
        sample_df,
        "Product",
        "Sales",
        3,
        False
    )

    assert result["selected_values"] == [
        "Laptop",
        "Phone",
        "Table",
    ]


def test_group_comparison(sample_df):
    result = group_comparison(
        sample_df,
        "Category",
        "Sales",
        "sum"
    )

    data = result["data"]

    assert data[0]["Category"] == "Furniture"
    assert data[0]["Sales"] == 25000


def test_percentage_share(sample_df):
    result = percentage_share(
        sample_df,
        "Category",
        "Sales"
    )

    technology = next(
        item
        for item in result["data"]
        if item["Category"] == "Technology"
    )

    assert technology["percentage"] == 76.19


def test_correlation(sample_df):
    result = correlation_analysis(
        sample_df,
        "Sales",
        "Profit"
    )

    assert result["correlation"] > 0.99

from app.tools.analysis_tools import (
    calculate_sum,
    calculate_average,
    top_n_analysis,
    group_comparison,
    percentage_share,
    correlation_analysis,
    filter_dataframe_by_values,
    filter_groups_by_metric,
    group_insight,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Product": [
            "Laptop",
            "Phone",
            "Table",
            "Chair",
        ],
        "Category": [
            "Technology",
            "Technology",
            "Furniture",
            "Furniture",
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
        "Region": [
            "West",
            "East",
            "West",
            "Central",
        ],
    })