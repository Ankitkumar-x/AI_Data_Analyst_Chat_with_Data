import pandas as pd

from app.tools.analysis_tools import (
    correlation_analysis
)


df = pd.DataFrame(
    {
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


result = correlation_analysis(
    df,
    column_x="Sales",
    column_y="Profit"
)


print("\nCORRELATION RESULT:")
print(result)