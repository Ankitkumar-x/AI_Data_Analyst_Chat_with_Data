import pandas as pd

from app.tools.analysis_tools import get_dataset_summary


df = pd.DataFrame(
    {
        "Order Date": [
            "2026-01-05",
            "2026-02-10",
            "2026-03-15",
            "2026-04-20"
        ],
        "Product": [
            "Laptop",
            "Phone",
            "Chair",
            "Table"
        ],
        "Sales": [
            50000,
            30000,
            10000,
            15000
        ]
    }
)


result = get_dataset_summary(df)


print("\nDATE DETECTION RESULT:")
print(result)