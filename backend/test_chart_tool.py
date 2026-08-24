import pandas as pd

from app.tools.chart_tools import create_bar_chart


df = pd.DataFrame(
    {
        "Product": [
            "Laptop",
            "Phone",
            "Chair",
            "Table"
        ],
        "Category": [
            "Technology",
            "Technology",
            "Furniture",
            "Furniture"
        ],
        "Sales": [
            50000,
            30000,
            10000,
            15000
        ],
        "Profit": [
            8000,
            5000,
            2000,
            3000
        ]
    }
)


result = create_bar_chart(
    df,
    category_column="Category",
    value_column="Sales",
    aggregation="sum"
)


print("\nCHART RESULT:")
print(result)