import io

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_upload_csv():

    csv_content = (
        "Product,Category,Sales,Profit,Region\n"
        "Laptop,Technology,50000,8000,West\n"
        "Phone,Technology,30000,5000,East\n"
        "Table,Furniture,15000,3000,West\n"
        "Chair,Furniture,10000,2000,Central\n"
    )

    response = client.post(
        "/api/upload",
        files={
            "file": (
                "test.csv",
                io.BytesIO(
                    csv_content.encode("utf-8")
                ),
                "text/csv"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test.csv"
    assert "profile" in data

    assert data["profile"]["rows"] == 4
    assert data["profile"]["columns"] == 5


def test_upload_invalid_file_type():

    response = client.post(
        "/api/upload",
        files={
            "file": (
                "test.txt",
                io.BytesIO(b"invalid file"),
                "text/plain"
            )
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert (
        data["detail"]
        == "Only CSV and Excel files are supported."
    )