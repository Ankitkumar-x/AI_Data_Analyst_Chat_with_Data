import io
import pandas as pd

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_full_application_flow():

    csv_content = (
        "Product,Category,Sales,Profit,Region\n"
        "Laptop,Technology,50000,8000,West\n"
        "Phone,Technology,30000,5000,East\n"
        "Table,Furniture,15000,3000,West\n"
        "Chair,Furniture,10000,2000,Central\n"
    )

    # 1. Upload
    upload_response = client.post(
        "/api/upload",
        files={
            "file": (
                "integration.csv",
                io.BytesIO(
                    csv_content.encode("utf-8")
                ),
                "text/csv",
            )
        },
    )

    assert upload_response.status_code == 200

    upload_data = upload_response.json()

    assert upload_data["profile"]["rows"] == 4
    assert upload_data["profile"]["columns"] == 5

    # 2. Dashboard summary
    dashboard_response = client.get(
        "/api/dashboard"
    )

    assert dashboard_response.status_code == 200

    dashboard_data = dashboard_response.json()

    assert dashboard_data["rows"] == 4
    assert "kpis" in dashboard_data
    assert "data_quality" in dashboard_data
    assert "numerical_statistics" in dashboard_data

    # 3. Dashboard visualizations
    visual_response = client.get(
        "/api/dashboard/visualizations"
    )

    assert visual_response.status_code == 200

    visual_data = visual_response.json()

    assert "charts" in visual_data
    assert len(visual_data["charts"]) > 0

    # 4. Chat
    chat_response = client.post(
        "/api/chat",
        json={
            "message": "What is the average Sales?",
            "conversation_history": [],
        },
    )

    assert chat_response.status_code == 200

    chat_data = chat_response.json()

    assert "answer" in chat_data
    assert "chart" in chat_data
    assert "26,250" in chat_data["answer"]