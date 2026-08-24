import pandas as pd

from app.tools.analysis_tools import percentage_share


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
        ]
    }
)


result = percentage_share(
    df,
    group_column="Category",
    value_column="Sales"
)


print("\nPERCENTAGE SHARE RESULT:")
print(result)