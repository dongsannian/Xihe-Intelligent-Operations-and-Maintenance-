# routers/alarm.py
from fastapi import APIRouter
router = APIRouter()

@router.get("/alarm/ping")
def ping():
    return {"ok": True}

