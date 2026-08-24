import pandas as pd

from app.tools.analysis_tools import correlation_analysis


df = pd.DataFrame(
    {
        "Sales": [
            100,
            100,
            100,
            100
        ],
        "Profit": [
            500,
            600,
            700,
            800
        ]
    }
)


try:

    result = correlation_analysis(
        df,
        column_x="Sales",
        column_y="Profit"
    )

    print("\nRESULT:")
    print(result)

except ValueError as error:

    print("\nEXPECTED ERROR:")
    print(error)