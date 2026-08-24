import pandas as pd

from app.ai.agent import analyze_question


df = pd.DataFrame(
    {
        "Product": [
            "Laptop",
            "Phone",
            "Chair",
            "Table"
        ],
        "Category": [
            "Technology",
            "Technology",
            "Furniture",
            "Furniture"
        ],
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
        ],
        "Region": [
            "North",
            "South",
            "West",
            "East"
        ]
    }
)

question = "What is the average Sales?"


answer = analyze_question(
    df,
    question
)


print("\nAI ANSWER:")
print(answer)