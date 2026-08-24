import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from app.data.dataset_manager import set_active_dataset


client = TestClient(app)


def setup_dataset():

    df = pd.DataFrame({
        "Product": [
            "Laptop",
            "Phone",
            "Table",
            "Chair",
        ],
        "Category": [
            "Technology",
            "Technology",
            "Furniture",
            "Furniture",
        ],
        "Sales": [
            50000,
            30000,
            15000,
            10000,
        ],
        "Profit": [
            8000,
            5000,
            3000,
            2000,
        ],
        "Region": [
            "West",
            "East",
            "West",
            "Central",
        ],
    })

    set_active_dataset(df)


def test_chat_average_sales():

    setup_dataset()

    response = client.post(
        "/api/chat",
        json={
            "message": "What is the average Sales?",
            "conversation_history": []
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "chart" in data

    assert "26,250" in data["answer"]


def test_chat_empty_message():

    setup_dataset()

    response = client.post(
        "/api/chat",
        json={
            "message": "   ",
            "conversation_history": []
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Message cannot be empty."


def test_chat_with_history():

    setup_dataset()

    response = client.post(
        "/api/chat",
        json={
            "message": "What about Profit?",
            "conversation_history": [
                {
                    "role": "user",
                    "content": "What is the average Sales?"
                },
                {
                    "role": "assistant",
                    "content": "The average Sales is 26,250."
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "4,500" in data["answer"]