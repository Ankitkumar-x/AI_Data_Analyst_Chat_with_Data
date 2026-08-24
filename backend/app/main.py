from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.dashboard import router as dashboard_router

from app.api.dashboard_visuals import router as dashboard_visuals_router

app = FastAPI(
    title="AI Data Analyst",
    description="Chat with your data using AI",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ai-chat-with-data.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    upload_router,
    prefix="/api"
)

app.include_router(
    chat_router,
    prefix="/api"
)

app.include_router(
    dashboard_router,
    prefix="/api"
)


app.include_router(
    dashboard_visuals_router,
    prefix="/api"
)


@app.get("/")
def root():
    return {
        "message": "AI Data Analyst API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

