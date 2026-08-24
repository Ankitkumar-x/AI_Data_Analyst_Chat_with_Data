import json

from app.ai.groq_client import client
from app.ai.tool_schemas import AVAILABLE_TOOLS


messages = [
    {
        "role": "system",
        "content": (
            "You are an AI Data Analyst. "
            "Use the available tools when the user's "
            "question requires calculations on their dataset."
        )
    },
    {
        "role": "user",
        "content": "Show me the Sales trend by Month."
    }
]


response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,
    tools=AVAILABLE_TOOLS,
    tool_choice="auto"
)


message = response.choices[0].message


print("Assistant message:")
print(message)

print("\nTool calls:")

if message.tool_calls:

    for tool_call in message.tool_calls:

        print("Tool name:")
        print(tool_call.function.name)

        print("Arguments:")
        print(tool_call.function.arguments)

else:

    print("No tool was called.")