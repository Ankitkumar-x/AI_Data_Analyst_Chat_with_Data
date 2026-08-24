import pandas as pd

from app.tools.analysis_tools import top_n_analysis


df = pd.DataFrame(
    {
        "Product": [
            "Laptop",
            "Phone",
            "Chair",
            "Table",
            "Monitor",
            "Keyboard"
        ],
        "Sales": [
            50000,
            30000,
            10000,
            15000,
            40000,
            12000
        ]
    }
)


result = top_n_analysis(
    df,
    group_column="Product",
    value_column="Sales",
    n=3
)


print("\nTOP N RESULT:")
print(result)