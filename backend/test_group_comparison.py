import pandas as pd

from app.tools.analysis_tools import group_comparison


df = pd.DataFrame(
    {
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


result = group_comparison(
    df,
    group_column="Category",
    value_column="Sales",
    aggregation="mean"
)


print("\nGROUP COMPARISON RESULT:")
print(result)