from dotenv import load_dotenv
from pathlib import Path

from fastapi import FastAPI

# Load project credentials before the route imports initialize application code.
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

from AI_Assistant.routes.chat import router as chat_router
from AI_Assistant.routes.health import health_check


app = FastAPI(title="AI Assistant API", version="1.0.0")
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(health_check, tags=["health"])




