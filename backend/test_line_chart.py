import pandas as pd

from app.tools.chart_tools import create_line_chart


df = pd.DataFrame(
    {
        "Month": [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May"
        ],
        "Sales": [
            20000,
            25000,
            31000,
            28000,
            35000
        ]
    }
)


result = create_line_chart(
    df,
    x_column="Month",
    value_column="Sales",
    aggregation="sum"
)


print("\nLINE CHART RESULT:")
print(result)