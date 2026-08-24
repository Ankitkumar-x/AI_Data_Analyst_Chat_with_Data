import pandas as pd

from app.ai.tool_executor import execute_tool_call


df = pd.DataFrame()


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

print("\nEMPTY DATASET RESULT:")
print(result)