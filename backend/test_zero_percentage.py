import pandas as pd

from app.tools.analysis_tools import percentage_share


df = pd.DataFrame(
    {
        "Category": [
            "A",
            "B",
            "C"
        ],
        "Sales": [
            0,
            0,
            0
        ]
    }
)


try:

    result = percentage_share(
        df,
        group_column="Category",
        value_column="Sales"
    )

    print("\nRESULT:")
    print(result)

except ValueError as error:

    print("\nEXPECTED ERROR:")
    print(error)