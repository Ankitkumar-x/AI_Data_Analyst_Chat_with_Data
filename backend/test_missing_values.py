import pandas as pd

from app.ai.tool_executor import execute_tool_call


df = pd.DataFrame(
    {
        "Product": [
            "Laptop",
            "Phone",
            "Chair",
            "Table"
        ],
        "Sales": [
            50000,
            None,
            10000,
            15000
        ],
        "Profit": [
            8000,
            5000,
            None,
            3000
        ]
    }
)


tool_call = type(
    "ToolCall",
    (),
    {
        "function": type(
            "Function",
            (),
            {
                "name": "get_dataset_summary",
                "arguments": "{}"
            }
        )()
    }
)()


result = execute_tool_call(
    tool_call,
    df
)


print("\nMISSING VALUES RESULT:")
print(result)