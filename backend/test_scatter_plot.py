import pandas as pd

from app.tools.chart_tools import create_scatter_plot


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


result = create_scatter_plot(
    df,
    x_column="Sales",
    y_column="Profit"
)


print("\nSCATTER PLOT RESULT:")
print(result)