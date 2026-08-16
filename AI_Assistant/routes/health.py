
from fastapi import APIRouter

health_check = APIRouter()

@health_check.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
