# routers/log.py
from fastapi import APIRouter
router = APIRouter()

@router.get("/log/ping")
def ping():
    return {"ok": True}

