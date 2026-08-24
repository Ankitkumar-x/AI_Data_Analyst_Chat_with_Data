from fastapi import APIRouter, HTTPException

from app.data.dataset_manager import get_active_dataset
from app.data.profiler import profile_dataset


router = APIRouter()


@router.get("/dashboard")
async def dashboard_summary():

    try:

        df = get_active_dataset()

        profile = profile_dataset(df)

        return profile

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred."
        )