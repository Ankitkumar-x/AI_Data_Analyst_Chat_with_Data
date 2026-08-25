from fastapi import APIRouter, HTTPException
from groq import RateLimitError
from pydantic import BaseModel, Field

from app.ai.agent import analyze_question
from app.data.dataset_manager import get_active_dataset


router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_history: list[dict] = []

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )

    conversation_history: list[dict] = Field(
        default_factory=list
    )


@router.post("/chat")
async def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:

        df = get_active_dataset()

        result = analyze_question(
            df,
            request.message,
            request.conversation_history
        )

        return {
            "answer": result["answer"],
            "chart": result["chart"]
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="The AI model has reached its current usage limit. Please try again shortly."
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred."
        )