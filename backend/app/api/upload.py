import tempfile
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

from pathlib import Path
import os

from fastapi import APIRouter, UploadFile, HTTPException

from app.data.dataset_manager import set_active_dataset

from app.data.loader import load_dataset
from app.data.profiler import profile_dataset


router = APIRouter()


@router.post("/upload")
async def upload_dataset(file: UploadFile):

    allowed_extensions = {".csv", ".xlsx", ".xls"}

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files are supported."
        )

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            contents = await file.read()

            if len(contents) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail="File size must not exceed 10 MB."
                )
            temp_file.write(contents)
            temp_path = temp_file.name

        df = load_dataset(temp_path)
        set_active_dataset(df)
        profile = profile_dataset(df)

        return {
            "filename": file.filename,
            "profile": profile
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred."
        )