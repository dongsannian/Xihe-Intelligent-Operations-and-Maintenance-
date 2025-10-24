# schemas.py
from pydantic import BaseModel

class RegisterIn(BaseModel):
    username: str
    password: str
    phone: str | None = None

class LoginIn(BaseModel):
    username: str
    password: str

class ResetIn(BaseModel):
    phone: str
    new_password: str

class StatusOut(BaseModel):
    status: dict
    gpuDetails: dict

